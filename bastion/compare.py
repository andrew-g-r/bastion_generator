"""Compare saved character revisions without mutating either record."""


def compare(before, after):
    left, right = before.to_dict(), after.to_dict()
    return {
        key: {"before": left[key], "after": right[key]} for key in left if left[key] != right[key]
    }
