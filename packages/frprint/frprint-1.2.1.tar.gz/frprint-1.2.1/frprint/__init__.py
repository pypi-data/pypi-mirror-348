from .frprint import frprint

# frprint 함수를 모듈 레벨로 가져옵니다
globals().update({"frprint": frprint})

__all__ = ["frprint"]