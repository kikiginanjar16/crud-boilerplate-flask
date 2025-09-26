
from typing import Tuple
from sqlalchemy import asc, desc

def apply_filters_sort_pagination(query, model, q=None, search_cols=None, sort="id", page=1, per_page=10):
    if q and search_cols:
        like=f"%{q}%"
        cond=None
        for col in search_cols:
            c=getattr(model, col, None)
            if c is not None:
                cond = (c.ilike(like)) if cond is None else (cond | c.ilike(like))
        if cond is not None:
            query=query.filter(cond)

    sort_cols=[]
    for token in (sort or "").split(","):
        token=token.strip()
        if not token: continue
        direction = desc if token.startswith("-") else asc
        colname = token[1:] if token.startswith("-") else token
        col=getattr(model, colname, None)
        if col is not None: sort_cols.append(direction(col))
    if sort_cols: query=query.order_by(*sort_cols)

    pagination=query.paginate(page=page, per_page=min(per_page, 100), error_out=False)
    return pagination
