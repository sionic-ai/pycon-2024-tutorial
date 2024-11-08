from collections import defaultdict
from typing import List


def merge_search_results(
    code_search_result: List[dict], nlu_search_result: List[dict]
) -> List[dict]:
    """Merge search results from code and NLU searchers

    Args:
        code_search_result (List[dict]): Code search results
            Examples:
                [
                    {"end_line": 127, "file": "lib/segment/src/index/query_estimator.rs", "start_line": 123}
                    {"end_line": 830, "file": "lib/segment/src/segment.rs", "start_line": 827}
                    {"end_line": 169, "file": "lib/segment/src/index/field_index/field_index_base.rs", "start_line": 166}
                    {"end_line": 162, "file": "lib/segment/src/index/query_estimator.rs", "start_line": 158}
                    {"end_line": 152, "file": "lib/collection/src/shards/local_shard_operations.rs", "start_line": 150}
                ]

        nlu_search_result (List[dict]): NLU search results
            Examples:
                [
                    {
                        "code_type": "Function",
                        "context": {
                            "file_name": "query_estimator.rs",
                            "file_path": "lib/segment/src/index/query_estimator.rs",
                            "module": "index",
                            "snippet": "...",
                            "struct_name": null
                        },
                        "docstring": null,
                        "line": 13,
                        "line_from": 13,
                        "line_to": 39,
                        "name": "combine_should_estimations",
                        "signature": "fn combine_should_estimations () -> CardinalityEstimation"
                    }
                ]
    """

    # 1. 파일 경로를 키로 하는 defaultdict 생성
    code_search_result_by_file = defaultdict(list)

    # 2. 코드 검색 결과를 파일별로 그룹화
    for hit in code_search_result:
        code_search_result_by_file[hit["file"]].append(hit)

    # 3. NLU 검색 결과를 순회하면서 매칭되는 코드 검색 결과 찾기
    for nlu_search_hit in nlu_search_result:
        # 4. NLU 결과의 파일 경로 추출
        file = nlu_search_hit["context"]["file_path"]

        # 5. 같은 파일에 코드 검색 결과가 있는지 확인
        if file in code_search_result_by_file:
            # 6. 중복되는 부분 찾아서 sub_matches에 추가
            nlu_search_hit["sub_matches"] = try_merge_overlapping_snippets(
                code_search_result_by_file[file], nlu_search_hit
            )

    # 7. sub_matches 개수가 많은 순으로 정렬
    nlu_search_result = sorted(
        nlu_search_result, key=lambda x: -len(x.get("sub_matches", []))
    )

    return nlu_search_result


def try_merge_overlapping_snippets(
    code_search_results: List[dict], nlu_search_result: dict
) -> List[dict]:
    """Find code search results that overlap with NLU search results and merge them

    Use nlu_search_result as a base for merging

    Args:
        code_search_results:
            [
                    {"end_line": 127, "start_line": 123, ...}
                    {"end_line": 830, "start_line": 827, ...}
                    {"end_line": 169, "start_line": 166, ...}
                    {"end_line": 162, "start_line": 158, ...}
                    {"end_line": 14, "start_line": 16, ...}
            ]
        nlu_search_result:
            {
                "line": 13,
                "line_from": 13,
                "line_to": 39,
                ...
            }

    Returns: Overlapping code search results merged with NLU search results
    """

    # 1. 중복 결과를 저장할 리스트 생성
    overlapped: list[dict[str, int]] = []

    # 2. 시작 라인 기준으로 코드 검색 결과 정렬
    code_search_result = sorted(code_search_results, key=lambda x: x["start_line"])

    # 3. 각 코드 검색 결과에 대해 중복 검사
    for code_search_hit in code_search_result:
        # 4. 라인 범위 계산 (1-based indexing으로 변환)
        from_a = code_search_hit["start_line"] + 1  # 코드 검색 범위 시작
        to_a = code_search_hit["end_line"] + 1  # 코드 검색 범위 끝
        from_b = nlu_search_result["line_from"]  # NLU 검색 범위 시작
        to_b = nlu_search_result["line_to"]  # NLU 검색 범위 끝

        # 5. 겹치는 범위 계산
        start = max(from_a, from_b)  # 더 뒤에 있는 시작점
        end = min(to_a, to_b)  # 더 앞에 있는 끝점

        # 6. 겹치는 부분이 있으면 결과에 추가
        if start <= end:
            overlapped.append(
                {
                    "overlap_from": start,
                    "overlap_to": end,
                }
            )

    return overlapped
