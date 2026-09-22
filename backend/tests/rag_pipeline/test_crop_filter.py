"""Post-retrieval crop filter (app.domain.crop_scope)."""
from app.domain.contracts import RetrievedSource
from app.domain.crop_scope import filter_by_crop, passage_crops


def _src(i, text):
    return RetrievedSource(id=f"t{i}", score=1.0, title_en=text, content_en=text)


def test_other_crop_dropped_neutral_and_same_crop_kept_in_order():
    srcs = [_src(1, "Potato late blight control"), _src(2, "Chilli leaf curl"),
            _src(3, "Soil pH management"), _src(4, "Potato and tomato blight")]
    kept, removed = filter_by_crop(srcs, "potato", 5)
    assert [s.id for s in kept] == ["t1", "t3", "t4"]
    assert removed == 1


def test_top_k_respected():
    srcs = [_src(i, "Potato scab") for i in range(10)]
    kept, _ = filter_by_crop(srcs, "potato", 5)
    assert len(kept) == 5


def test_no_crop_or_unknown_crop_is_passthrough():
    srcs = [_src(1, "Chilli leaf curl"), _src(2, "Rice blast")]
    assert filter_by_crop(srcs, None, 5)[0] == srcs
    assert filter_by_crop(srcs, "dragonfruit_unknown", 5)[0] == srcs


def test_bengali_alias_detected():
    assert "potato" in passage_crops(_src(9, "আলুর মড়ক রোগ"))
