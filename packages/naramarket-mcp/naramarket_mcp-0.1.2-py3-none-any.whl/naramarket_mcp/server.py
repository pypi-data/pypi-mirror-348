# naramarket_mcp_server.py
import os
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import logging
from urllib.parse import unquote
import argparse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 초기화
mcp = FastMCP("나라장터 입찰 공고 검색 MCP 서버")

# API 기본 URL
BASE_URL = "http://apis.data.go.kr/1230000/ad/BidPublicInfoService"

# 입찰 공고 타입 별 세부 엔드포인트
BID_ENDPOINTS = {
    "공사": "getBidPblancListInfoCnstwkPPSSrch",
    "용역": "getBidPblancListInfoServcPPSSrch",
    "외자": "getBidPblancListInfoFrgcptPPSSrch",
    "물품": "getBidPblancListInfoThngPPSSrch"
}


# 환경변수 설정 및 SERVICE_KEY 초기화 함수
def initialize_environment():
    # 기본 .env 파일 로드 (이 부분은 먼저 시도해보는 것이 좋음)
    load_dotenv()
    
    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(description="나라장터 입찰 공고 검색 MCP 서버")
    parser.add_argument("--service-key", help="나라장터 API 서비스 키")
    parser.add_argument("--env-file", help=".env 파일 경로 (기본값: .env)")
    args = parser.parse_args()
    
    # 사용자 지정 .env 파일이 있다면 로드
    if args.env_file and os.path.exists(args.env_file):
        logger.info(f"{args.env_file} 파일에서 환경변수를 로드합니다.")
        load_dotenv(args.env_file, override=True)
    
    # 명령줄에서 service-key가 제공되면 환경변수로 설정
    if args.service_key:
        logger.info("명령줄에서 제공된 SERVICE_KEY를 사용합니다.")
        os.environ["SERVICE_KEY"] = args.service_key
    
    # 환경변수에서 API 키 가져오기
    service_key = os.getenv("SERVICE_KEY")
    if not service_key:
        logger.error("SERVICE_KEY 환경변수가 설정되지 않았습니다.")
        raise ValueError("SERVICE_KEY 환경변수가 설정되지 않았습니다. --service-key 옵션이나 .env 파일을 통해 설정해주세요.")
    
    return unquote(service_key)

# 전역 변수 선언 (실행 시 initialize_environment()에서 할당됨)
DECODED_SERVICE_KEY = None



# XML 응답을 파싱하는 함수
async def parse_xml_response(xml_content: str) -> Dict:
    try:
        root = ET.fromstring(xml_content)
        result = {}
        
        # 헤더 정보 추출
        header = root.find(".//header")
        if header is not None:
            result_code = header.find("resultCode")
            result_msg = header.find("resultMsg")
            if result_code is not None:
                result["resultCode"] = result_code.text
            if result_msg is not None:
                result["resultMsg"] = result_msg.text
        
        # 바디 정보 추출
        body = root.find(".//body")
        if body is not None:
            items_tag = body.find("items")
            if items_tag is not None:
                items = []
                for item_tag in items_tag.findall("item"):
                    item = {}
                    for child in item_tag:
                        item[child.tag] = child.text
                    items.append(item)
                result["items"] = items
            
            # 페이징 정보 추출
            num_of_rows = body.find("numOfRows")
            page_no = body.find("pageNo")
            total_count = body.find("totalCount")
            
            if num_of_rows is not None:
                result["numOfRows"] = int(num_of_rows.text)
            if page_no is not None:
                result["pageNo"] = int(page_no.text)
            if total_count is not None:
                result["totalCount"] = int(total_count.text)
        
        return result
    except ET.ParseError as e:
        logger.error(f"XML 파싱 오류: {e}")
        logger.debug(f"XML 내용: {xml_content[:500]}...")
        raise Exception(f"XML 응답 파싱 중 오류가 발생했습니다: {e}")

@mcp.tool()
async def search_bids(
    ctx: Context,
    keyword: str,
    bid_type: str = "물품",
    page: int = 1,
    rows: int = 10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    나라장터에서 입찰 공고를 검색합니다.
    
    Args:
        keyword: 검색할 키워드 (입찰공고명에 포함될 단어)
        bid_type: 입찰 종류 (공사, 용역, 외자, 물품)
        page: 페이지 번호
        rows: 한 페이지 결과 수
        start_date: 조회 시작일 (YYYYMMDD 형식)
        end_date: 조회 종료일 (YYYYMMDD 형식)
        
    Returns:
        입찰 공고 정보가 담긴 딕셔너리
    """
    ctx.info(f"'{keyword}' 키워드로 {bid_type} 입찰 공고를 검색 중...")
    
    if bid_type not in BID_ENDPOINTS:
        ctx.error(f"지원하지 않는 입찰 종류입니다: {bid_type}")
        return {"error": f"지원하지 않는 입찰 종류입니다. 지원 종류: {', '.join(BID_ENDPOINTS.keys())}"}
    
    # 날짜 형식 변환
    inqry_begin_dt = f"{start_date}0000" if start_date else (datetime.now() - timedelta(days=30)).strftime("%Y%m%d0000")
    inqry_end_dt = f"{end_date}2359" if end_date else datetime.now().strftime("%Y%m%d2359")
    
    endpoint = BID_ENDPOINTS[bid_type]
    url = f"{BASE_URL}/{endpoint}"
    
    params = {
        "serviceKey": DECODED_SERVICE_KEY,
        "numOfRows": rows,
        "pageNo": page,
        "inqryDiv": "1",  # 1: 공고게시일시, 2: 개찰일시
        "bidNtceNm": keyword,  # 입찰공고명에 키워드 검색
        "inqryBgnDt": inqry_begin_dt,
        "inqryEndDt": inqry_end_dt,
    }
    
    try:
        ctx.info("나라장터 API 호출 중...")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            # 응답을 XML에서 딕셔너리로 파싱
            result = await parse_xml_response(response.text)
            
            # 결과 코드 확인
            if "resultCode" in result and result["resultCode"] != "00":
                ctx.error(f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}")
                return {"error": f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}"}
            
            ctx.info(f"총 {result.get('totalCount', 0)}개의 결과를 찾았습니다.")
            
            # 결과가 없는 경우
            if result.get("totalCount", 0) == 0 or not result.get("items"):
                return {
                    "totalCount": 0,
                    "message": "검색 결과가 없습니다.",
                    "items": []
                }
            
            # 응답 데이터 구성
            return {
                "totalCount": result.get("totalCount", 0),
                "numOfRows": result.get("numOfRows", rows),
                "pageNo": result.get("pageNo", page),
                "items": result.get("items", [])
            }
            
    except httpx.HTTPStatusError as e:
        ctx.error(f"HTTP 오류: {e}")
        return {"error": f"API 요청 중 HTTP 오류가 발생했습니다: {e}"}
    except httpx.RequestError as e:
        ctx.error(f"요청 오류: {e}")
        return {"error": f"API 요청 중 오류가 발생했습니다: {e}"}
    except Exception as e:
        ctx.error(f"예외 발생: {e}")
        return {"error": f"오류가 발생했습니다: {e}"}

@mcp.tool()
async def get_bid_details(
    ctx: Context,
    bid_notice_no: str,
    bid_notice_ord: str = "01",
) -> Dict[str, Any]:
    """
    나라장터에서 특정 입찰 공고의 상세 정보를 조회합니다.
    
    Args:
        bid_notice_no: 입찰공고번호
        bid_notice_ord: 입찰공고차수 (기본값: 01)
        
    Returns:
        입찰 공고 상세 정보가 담긴 딕셔너리
    """
    ctx.info(f"입찰공고번호 {bid_notice_no}, 차수 {bid_notice_ord}의 상세 정보를 조회 중...")
    
    # 모든 입찰 유형에 대해 검색 (상세 정보를 찾기 위해)
    for bid_type, endpoint in BID_ENDPOINTS.items():
        url = f"{BASE_URL}/{endpoint}"
        
        params = {
            "serviceKey": DECODED_SERVICE_KEY,
            "numOfRows": 10,
            "pageNo": 1,
            "inqryDiv": "1",
            "bidNtceNo": bid_notice_no
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                
                result = await parse_xml_response(response.text)
                
                if "resultCode" in result and result["resultCode"] != "00":
                    continue  # 다음 입찰 유형으로 시도
                
                # 결과에서 해당 공고번호와 차수를 가진 항목 찾기
                items = result.get("items", [])
                for item in items:
                    if item.get("bidNtceNo") == bid_notice_no and item.get("bidNtceOrd") == bid_notice_ord:
                        ctx.info(f"{bid_type} 유형에서 입찰 공고를 찾았습니다.")
                        return {
                            "bid_type": bid_type,
                            "details": item
                        }
                
        except Exception as e:
            ctx.error(f"{bid_type} 유형 검색 중 오류: {e}")
            continue  # 다음 입찰 유형으로 시도
    
    # 모든 유형을 검색했지만 찾지 못한 경우
    ctx.error(f"입찰공고번호 {bid_notice_no}, 차수 {bid_notice_ord}의 정보를 찾을 수 없습니다.")
    return {"error": "해당 입찰 공고를 찾을 수 없습니다."}

@mcp.tool()
async def search_by_organization(
    ctx: Context,
    organization_name: str,
    bid_type: str = "물품",
    is_demand_org: bool = False,
    page: int = 1,
    rows: int = 10,
) -> Dict[str, Any]:
    """
    특정 기관이 등록한 입찰 공고를 검색합니다.
    
    Args:
        organization_name: 기관명
        bid_type: 입찰 종류 (공사, 용역, 외자, 물품)
        is_demand_org: True면 수요기관, False면 공고기관으로 검색
        page: 페이지 번호
        rows: 한 페이지 결과 수
        
    Returns:
        해당 기관의 입찰 공고 정보가 담긴 딕셔너리
    """
    ctx.info(f"'{organization_name}' 기관의 {bid_type} 입찰 공고를 검색 중...")
    
    if bid_type not in BID_ENDPOINTS:
        ctx.error(f"지원하지 않는 입찰 종류입니다: {bid_type}")
        return {"error": f"지원하지 않는 입찰 종류입니다. 지원 종류: {', '.join(BID_ENDPOINTS.keys())}"}
    
    endpoint = BID_ENDPOINTS[bid_type]
    url = f"{BASE_URL}/{endpoint}"
    
    # 최근 3개월 기간으로 설정
    inqry_begin_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d0000")
    inqry_end_dt = datetime.now().strftime("%Y%m%d2359")
    
    params = {
        "serviceKey": DECODED_SERVICE_KEY,
        "numOfRows": rows,
        "pageNo": page,
        "inqryDiv": "1",
    }
    
    # 수요기관 또는 공고기관으로 검색
    if is_demand_org:
        params["dminsttNm"] = organization_name
    else:
        params["ntceInsttNm"] = organization_name
    
    params["inqryBgnDt"] = inqry_begin_dt
    params["inqryEndDt"] = inqry_end_dt
    
    try:
        ctx.info("나라장터 API 호출 중...")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            result = await parse_xml_response(response.text)
            
            if "resultCode" in result and result["resultCode"] != "00":
                ctx.error(f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}")
                return {"error": f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}"}
            
            org_type = "수요기관" if is_demand_org else "공고기관"
            ctx.info(f"{org_type} '{organization_name}'의 총 {result.get('totalCount', 0)}개 결과를 찾았습니다.")
            
            return {
                "organization_name": organization_name,
                "organization_type": org_type,
                "totalCount": result.get("totalCount", 0),
                "numOfRows": result.get("numOfRows", rows),
                "pageNo": result.get("pageNo", page),
                "items": result.get("items", [])
            }
            
    except Exception as e:
        ctx.error(f"예외 발생: {e}")
        return {"error": f"오류가 발생했습니다: {e}"}

@mcp.tool()
async def search_by_price_range(
    ctx: Context,
    min_price: int,
    max_price: int,
    bid_type: str = "물품",
    page: int = 1,
    rows: int = 10,
) -> Dict[str, Any]:
    """
    특정 가격 범위의 입찰 공고를 검색합니다.
    
    Args:
        min_price: 최소 추정가격 (원)
        max_price: 최대 추정가격 (원)
        bid_type: 입찰 종류 (공사, 용역, 외자, 물품)
        page: 페이지 번호
        rows: 한 페이지 결과 수
        
    Returns:
        가격 범위에 맞는 입찰 공고 정보가 담긴 딕셔너리
    """
    ctx.info(f"{min_price}원 ~ {max_price}원 범위의 {bid_type} 입찰 공고를 검색 중...")
    
    if bid_type not in BID_ENDPOINTS:
        ctx.error(f"지원하지 않는 입찰 종류입니다: {bid_type}")
        return {"error": f"지원하지 않는 입찰 종류입니다. 지원 종류: {', '.join(BID_ENDPOINTS.keys())}"}
    
    endpoint = BID_ENDPOINTS[bid_type]
    url = f"{BASE_URL}/{endpoint}"
    
    # 최근 3개월 기간으로 설정
    inqry_begin_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d0000")
    inqry_end_dt = datetime.now().strftime("%Y%m%d2359")
    
    params = {
        "serviceKey": DECODED_SERVICE_KEY,
        "numOfRows": rows,
        "pageNo": page,
        "inqryDiv": "1",
        "presmptPrceBgn": str(min_price),
        "presmptPrceEnd": str(max_price),
        "inqryBgnDt": inqry_begin_dt,
        "inqryEndDt": inqry_end_dt,
    }
    
    try:
        ctx.info("나라장터 API 호출 중...")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            result = await parse_xml_response(response.text)
            
            if "resultCode" in result and result["resultCode"] != "00":
                ctx.error(f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}")
                return {"error": f"API 오류: {result.get('resultMsg', '알 수 없는 오류')}"}
            
            ctx.info(f"가격 범위 내 총 {result.get('totalCount', 0)}개 결과를 찾았습니다.")
            
            return {
                "price_range": f"{min_price}원 ~ {max_price}원",
                "totalCount": result.get("totalCount", 0),
                "numOfRows": result.get("numOfRows", rows),
                "pageNo": result.get("pageNo", page),
                "items": result.get("items", [])
            }
            
    except Exception as e:
        ctx.error(f"예외 발생: {e}")
        return {"error": f"오류가 발생했습니다: {e}"}

# @mcp.resource(uri="/bid_type_options")
# def bid_type_options() -> Dict[str, str]:
#     """
#     입찰 공고 타입 옵션을 제공합니다.
#     """
#     return BID_ENDPOINTS

# @mcp.prompt(uri="/bid_search_template")
# def get_bid_search_template() -> str:
#     """
#     입찰 공고 검색에 활용할 수 있는 프롬프트 템플릿을 제공합니다.
#     """
#     return """
#     # 나라장터 입찰 공고 검색
    
#     다음 정보를 바탕으로 입찰 공고를 검색해주세요:
    
#     1. 검색 키워드: [키워드를 입력하세요]
#     2. 입찰 종류: [공사/용역/외자/물품 중 선택]
#     3. 페이지 번호: [숫자, 기본값은 1]
#     4. 검색 결과 수: [한 페이지당 결과 수, 기본값은 10]
#     5. 검색 시작일: [YYYYMMDD 형식, 선택사항]
#     6. 검색 종료일: [YYYYMMDD 형식, 선택사항]
    
#     검색 결과에서 다음 정보를 요약해주세요:
#     - 공고 수
#     - 주요 공고들의 제목, 기관명, 마감일
#     - 가장 큰 금액의 공고 정보
#     """

def main():
    """
    MCP 서버 메인 함수
    """
    global DECODED_SERVICE_KEY
    
    try:
        # 환경변수 초기화 및 SERVICE_KEY 설정
        DECODED_SERVICE_KEY = initialize_environment()
        logger.info("나라장터 MCP 서버를 시작합니다...")
        
        # 서버 실행
        mcp.run()
    except ValueError as e:
        logger.error(f"초기화 오류: {e}")
        print(f"오류: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"서버 실행 중 오류 발생: {e}")
        print(f"서버 실행 중 오류가 발생했습니다: {e}")
        exit(1)

if __name__ == "__main__":
    main()