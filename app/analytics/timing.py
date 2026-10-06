from __future__ import annotations
import pandas as pd

def first_touch_distribution(intraday: pd.DataFrame, level_col: str = "target", min_samples: int = 40) -> dict:
    """Expected input: rows with session, first_touch_minute (minutes after 09:15), touched bool.
    Production deployment should generate this table from historical intraday bars per setup family.
    """
    if intraday is None or len(intraday) < min_samples:
        return {"status":"INSUFFICIENT_DATA","sample_count":0 if intraday is None else len(intraday)}
    touched = intraday[intraday["touched"] == True]
    if touched.empty: return {"status":"OK","touch_probability":0.0,"buckets":{}}
    bins=[0,30,75,135,195,255,315,375]
    labels=["09:15-09:45","09:45-10:30","10:30-11:30","11:30-12:30","12:30-13:30","13:30-14:30","14:30-15:30"]
    cat=pd.cut(touched.first_touch_minute,bins=bins,labels=labels,right=False)
    dist=(cat.value_counts(normalize=True,sort=False)*100).round(1).to_dict()
    return {"status":"OK","sample_count":len(intraday),"touch_probability":round(len(touched)/len(intraday),3),"buckets":dist}
