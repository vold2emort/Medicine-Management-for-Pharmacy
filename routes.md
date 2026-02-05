Admin API Summary

API	                    Method	        Purpose
/api/medicines/	        POST	        Add medicine (with image)
/api/medicines/	        GET	            Get all
/api/medicines/{id}/	GET	            Single medicine
/api/medicines/{id}/	DELETE	        Remove
/api/expiry-alerts/	    GET	            Expiry warnings
/api/forecast/	        POST	        Demand forecast


forecast Usuage:

Test Demand Forecast API (Moving Average)

Open:

http://127.0.0.1:8000/api/forecast/


Use POST with JSON.

Paste this in request body:
```
{
  "medicine_id": 1,
  "past_sales": [20, 25, 22, 30, 28],
  "window_size": 3,
  "reorder_level": 15
}
```


Click POST.