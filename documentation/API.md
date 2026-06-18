# REST API Documentation

Complete REST API reference for Customer Churn Prediction application.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All API endpoints require an API key in the header:

```
X-API-Key: demo-key-12345
Content-Type: application/json
```

## Response Format

All responses are in JSON format:

### Success Response

```json
{
  "status": "success",
  "timestamp": "2026-06-18T10:30:00",
  "data": {}
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Error description"
}
```

## Endpoints

### 1. Make Prediction

**POST** `/api/predict`

Make a prediction for customer churn.

**Request Body:**

```json
{
  "contract_id": "CUST001",
  "tenure_months": 12,
  "monthly_charges": 65.5,
  "total_charges": 786.0,
  "age": 40,
  "internet_service": "Fiber optic",
  "phone_service": "Yes",
  "online_security": "No",
  "online_backup": "Yes",
  "device_protection": "No",
  "tech_support": "No",
  "streaming_tv": "No",
  "streaming_movies": "No",
  "contract": "Month-to-month",
  "paperless_billing": "Yes",
  "payment_method": "Electronic check",
  "save_prediction": true
}
```

**Response:**

```json
{
  "status": "success",
  "timestamp": "2026-06-18T10:30:00",
  "data": {
    "customer_id": null,
    "contract_id": "CUST001",
    "churn_prediction": "No",
    "churn_probability": 0.215,
    "risk_level": "Low Risk",
    "confidence_score": 0.92,
    "message": "Customer has Low Risk for churn"
  }
}
```

**Parameters:**

- `contract_id` (required): Customer contract ID
- `tenure_months` (required): Months as customer
- `monthly_charges` (required): Monthly charges amount
- `total_charges` (required): Total charges amount
- Other fields: Optional, defaults provided

**Status Codes:**

- `200` - Success
- `400` - Bad request
- `401` - Unauthorized
- `500` - Server error

---

### 2. Get Predictions

**GET** `/api/predictions`

Retrieve prediction history.

**Query Parameters:**

```
?limit=20&offset=0&risk_level=High Risk
```

- `limit` (optional): Records per page (default: 20)
- `offset` (optional): Pagination offset (default: 0)
- `risk_level` (optional): Filter by risk level

**Response:**

```json
{
  "status": "success",
  "timestamp": "2026-06-18T10:30:00",
  "total": 150,
  "limit": 20,
  "offset": 0,
  "data": [
    {
      "prediction_id": 1,
      "contract_id": "CUST001",
      "churn_prediction": 1,
      "churn_probability": 0.875,
      "risk_level": "High Risk",
      "model_name": "Random Forest",
      "confidence_score": 0.95,
      "prediction_timestamp": "2026-06-18 10:15:00"
    }
  ]
}
```

---

### 3. Get Customers

**GET** `/api/customers`

Retrieve customer list.

**Query Parameters:**

```
?limit=20&offset=0
```

**Response:**

```json
{
  "status": "success",
  "timestamp": "2026-06-18T10:30:00",
  "total": 75,
  "limit": 20,
  "offset": 0,
  "data": [
    {
      "customer_id": 1,
      "contract_id": "CUST001",
      "gender": "Male",
      "age": 65,
      "tenure_months": 2,
      "internet_service": "Fiber optic",
      "monthly_charges": 70.7,
      "total_charges": 1397.0
    }
  ]
}
```

---

### 4. Export Predictions

**GET** `/api/export/predictions`

Export all predictions in specified format.

**Query Parameters:**

```
?format=csv
```

- `format`: `csv` or `pdf` (default: csv)

**Response:**

- CSV: Returns CSV file download
- PDF: Returns PDF file download

**Example:**

```bash
curl -X GET "http://localhost:5000/api/export/predictions?format=csv" \
  -H "X-API-Key: demo-key-12345" \
  -o predictions.csv
```

---

### 5. Health Check

**GET** `/api/health`

Check API and system health.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2026-06-18T10:30:00",
  "database": "connected",
  "model": "loaded"
}
```

---

## Error Codes

| Code | Meaning             | Solution                                 |
| ---- | ------------------- | ---------------------------------------- |
| 400  | Bad Request         | Check request format and required fields |
| 401  | Unauthorized        | Verify API key in header                 |
| 404  | Not Found           | Check endpoint URL                       |
| 500  | Server Error        | Check server logs                        |
| 503  | Service Unavailable | Check database/model status              |

## Rate Limiting

Currently no rate limiting. In production, implement:

- 100 requests per minute per API key
- 5000 requests per hour per API key

## Examples

### Python

```python
import requests
import json

url = "http://localhost:5000/api/predict"
headers = {
    "X-API-Key": "demo-key-12345",
    "Content-Type": "application/json"
}

data = {
    "contract_id": "CUST001",
    "tenure_months": 12,
    "monthly_charges": 65.5,
    "total_charges": 786.0,
    "internet_service": "Fiber optic"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(f"Churn Probability: {result['data']['churn_probability']}")
print(f"Risk Level: {result['data']['risk_level']}")
```

### JavaScript

```javascript
const apiKey = "demo-key-12345";
const url = "http://localhost:5000/api/predict";

const data = {
  contract_id: "CUST001",
  tenure_months: 12,
  monthly_charges: 65.5,
  total_charges: 786.0,
  internet_service: "Fiber optic",
};

fetch(url, {
  method: "POST",
  headers: {
    "X-API-Key": apiKey,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})
  .then((response) => response.json())
  .then((result) => {
    console.log(`Risk Level: ${result.data.risk_level}`);
    console.log(`Probability: ${result.data.churn_probability}`);
  });
```

### cURL

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "CUST001",
    "tenure_months": 12,
    "monthly_charges": 65.5,
    "total_charges": 786.0,
    "internet_service": "Fiber optic",
    "phone_service": "Yes",
    "contract": "Month-to-month"
  }'
```

## Webhooks (Future)

Planned webhook support for real-time predictions:

- POST to custom endpoint on prediction
- Retry with exponential backoff
- Webhook signatures for security

## Versioning

Current version: `v1.0`

Future versions will support:

- API versioning (v2, v3, etc.)
- Backward compatibility
- Deprecation warnings

---

**Last Updated**: June 2026  
**API Version**: 1.0.0  
**Status**: Stable ✅
