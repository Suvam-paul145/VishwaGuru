# Field Officer Check-In System with Location Verification

**Issue #288** - Implementation Documentation

## Overview

The Field Officer Check-In System provides GPS-based verification of field officer visits to civic issue sites. This feature introduces location-based accountability, geo-fencing validation, public transparency, and immutable visit records.

## Key Features

### 1. **GPS-Based Check-In/Check-Out**
- Officers check in with GPS coordinates when visiting an issue site
- Check-out captures visit duration and location
- Automatic distance calculation from issue site
- Blockchain-style immutable visit hash for integrity

### 2. **Geo-Fencing Verification**
- Configurable radius validation (default: 100 meters)
- Haversine formula for accurate distance calculation
- Real-time verification of officer proximity to site
- Distance stored in meters with 2 decimal precision

### 3. **Public Transparency**
- All visit records are public by default (`is_public=True`)
- Citizens can view complete visit history for any issue
- Timestamped check-in/check-out records
- Officer details (name, department, designation) visible

### 4. **Visit Documentation**
- Upload up to 10 images per visit
- Visit notes for documenting observations
- Additional notes at check-out
- Verified visits by supervisors/admins

### 5. **Analytics & Metrics**
- Aggregate statistics across all visits
- Geo-fence compliance rates
- Average visit durations
- Verification status tracking

## Technical Implementation

### Database Model: `FieldOfficerVisit`

Located in: `backend/models.py`

**Key Fields:**
```python
- id: Primary key
- issue_id: Foreign key to Issue (required)
- grievance_id: Foreign key to Grievance (optional)
- officer_email: Officer's email (required)
- officer_name: Officer's full name (required)
- officer_department: Department (optional)
- officer_designation: Designation (optional)
- check_in_latitude: Check-in GPS latitude (required)
- check_in_longitude: Check-in GPS longitude (required)
- check_in_time: Timestamp of check-in
- check_out_latitude: Check-out GPS latitude (optional)
- check_out_longitude: Check-out GPS longitude (optional)
- check_out_time: Timestamp of check-out (optional)
- distance_from_site: Calculated distance in meters
- within_geofence: Boolean - inside acceptable radius
- geofence_radius_meters: Allowed radius (default: 100m)
- visit_notes: Text notes from officer
- visit_images: JSON array of image paths
- visit_duration_minutes: Duration of visit
- visit_hash: SHA-256 immutable integrity hash
- status: Enum (checked_in, checked_out, verified)
- verified_by: Email of verifier (admin/supervisor)
- verified_at: Timestamp of verification
- is_public: Boolean (default: True for transparency)
```

**Indexes for Performance:**
- `ix_field_officer_visits_issue_id` - Query visits by issue
- `ix_field_officer_visits_officer_email` - Officer visit history
- `ix_field_officer_visits_status` - Filter by status
- `ix_field_officer_visits_check_in_time` - Chronological queries

### Geo-Fencing Service

Located in: `backend/geofencing_service.py`

**Core Functions:**

1. **`calculate_distance(lat1, lon1, lat2, lon2)` → float**
   - Uses Haversine formula for great-circle distance
   - Accounts for Earth's curvature (radius: 6,371 km)
   - Returns distance in meters

2. **`is_within_geofence(check_in_lat, check_in_lon, site_lat, site_lon, radius_meters)` → (bool, float)**
   - Validates if check-in location is within allowed radius
   - Returns tuple: (within_fence, distance_in_meters)

3. **`generate_visit_hash(visit_data)` → str**
   - Creates SHA-256 hash from visit metadata
   - Ensures immutability of visit records
   - Blockchain-inspired integrity verification

4. **`calculate_visit_metrics(visits)` → dict**
   - Aggregates statistics across multiple visits
   - Returns total visits, average distance, compliance rate, etc.

### API Endpoints

Located in: `backend/routers/field_officer.py`

#### 1. **POST** `/api/field-officer/check-in`

Check in at an issue site with GPS verification.

**Request Body:**
```json
{
  "issue_id": 123,
  "officer_email": "officer@example.com",
  "officer_name": "John Doe",
  "officer_department": "Public Works",
  "officer_designation": "Field Inspector",
  "check_in_latitude": 19.0760,
  "check_in_longitude": 72.8777,
  "visit_notes": "Inspecting pothole reported by citizens",
  "geofence_radius_meters": 100,
  "grievance_id": 456  // Optional
}
```

**Response:**
```json
{
  "id": 789,
  "issue_id": 123,
  "officer_name": "John Doe",
  "check_in_time": "2024-01-15T10:30:00Z",
  "distance_from_site": 45.23,
  "within_geofence": true,
  "status": "checked_in",
  "visit_hash": "abc123...",
  ...
}
```

**Validations:**
- Issue must exist
- GPS coordinates must be valid (-90 to 90 lat, -180 to 180 lon)
- Issue must have location data for geo-fence verification
- Auto-calculates distance and within_geofence status

#### 2. **POST** `/api/field-officer/check-out`

Check out from a visit.

**Request Body:**
```json
{
  "visit_id": 789,
  "check_out_latitude": 19.0761,
  "check_out_longitude": 72.8778,
  "visit_duration_minutes": 45,
  "additional_notes": "Issue resolved. Pothole filled."
}
```

**Validations:**
- Visit must exist and not already checked out
- GPS coordinates validation
- Appends additional notes to visit

#### 3. **POST** `/api/field-officer/visit/{visit_id}/upload-images`

Upload visit documentation images.

**Request:**
- Multipart form data
- Up to 10 images per visit
- Images validated (must be image/* content type)

**Response:**
```json
{
  "visit_id": 789,
  "image_paths": [
    "data/visit_images/visit_789_20240115_103000_0.jpg",
    "data/visit_images/visit_789_20240115_103000_1.jpg"
  ],
  "message": "Successfully uploaded 2 images"
}
```

**Security:**
- Secure filename generation with timestamp
- Stored in `backend/data/visit_images/`

#### 4. **GET** `/api/field-officer/issue/{issue_id}/visit-history`

Get public visit history for an issue.

**Query Parameters:**
- `public_only=true` (default) - Only show public visits

**Response:**
```json
{
  "issue_id": 123,
  "total_visits": 3,
  "visits": [
    {
      "id": 789,
      "officer_name": "John Doe",
      "check_in_time": "2024-01-15T10:30:00Z",
      "check_out_time": "2024-01-15T11:15:00Z",
      "within_geofence": true,
      "distance_from_site": 45.23,
      "status": "verified",
      ...
    }
  ]
}
```

**Use Case:** Citizens can verify that officers have actually visited the site.

#### 5. **GET** `/api/field-officer/visit-stats`

Get aggregate statistics for all visits.

**Response:**
```json
{
  "total_visits": 150,
  "total_within_geofence": 142,
  "total_outside_geofence": 8,
  "compliance_rate": 94.67,
  "average_distance_from_site": 52.3,
  "total_verified": 130,
  "total_unverified": 20,
  "average_visit_duration_minutes": 38.5
}
```

#### 6. **POST** `/api/field-officer/visit/{visit_id}/verify`

Admin/supervisor verification of a visit.

**Request Body:**
```json
{
  "verifier_email": "supervisor@example.com"
}
```

**Effect:**
- Sets `verified_by` and `verified_at` fields
- Changes status to 'verified'

## Request/Response Schemas

Located in: `backend/schemas.py`

1. **`OfficerCheckInRequest`** - Check-in data validation
2. **`OfficerCheckOutRequest`** - Check-out data validation
3. **`FieldOfficerVisitResponse`** - Complete visit record
4. **`VisitHistoryResponse`** - List of visits for an issue
5. **`VisitStatsResponse`** - Aggregate statistics
6. **`VisitImageUploadResponse`** - Image upload result

**Validation Rules:**
- Latitude: -90.0 to 90.0
- Longitude: -180.0 to 180.0
- Geofence radius: 10 to 1000 meters
- Visit duration: 0 to 1440 minutes (24 hours)

## Database Migrations

Located in: `backend/init_db.py`

The migration script:
1. Checks if `field_officer_visits` table exists
2. Creates table if missing using SQLAlchemy model
3. Creates performance indexes:
   - `issue_id` - Fast lookup of visits by issue
   - `officer_email` - Officer visit history
   - `status` - Filter by visit status
   - `check_in_time` - Chronological ordering

Run migrations:
```bash
python -m backend.init_db
```

## Integration with Main Application

The router is registered in `backend/main.py`:

```python
from backend.routers import field_officer

app.include_router(field_officer.router, tags=["Field Officer Check-In"])
```

## Security & Privacy Considerations

### Public Transparency
- All visits are public by default (`is_public=True`)
- Citizens can verify officer visits to their reported issues
- Enhances accountability and trust

### Data Integrity
- Immutable visit hash (SHA-256) prevents tampering
- Hash includes: issue_id, officer_email, check-in coords, timestamp, notes
- Blockchain-inspired integrity verification

### GPS Validation
- Coordinate range validation
- Distance calculation using geodesic formula (not Euclidean)
- Configurable geo-fence radius (10-1000m)

### File Upload Security
- Secure filename generation (timestamp-based)
- Content type validation (images only)
- Maximum 10 images per visit
- Files stored outside web root

## Use Cases

### 1. **Citizen Verification**
A citizen reports a pothole. They can later:
- View visit history: `/api/field-officer/issue/123/visit-history`
- See when officers visited
- Check geo-fence compliance
- View visit photos

### 2. **Officer Accountability**
Field officers:
- Check in when arriving at site
- System verifies they're within 100m
- Document visit with notes and photos
- Check out when leaving

### 3. **Supervisor Oversight**
Supervisors/admins:
- Review all visits: `/api/field-officer/visit-stats`
- Verify visits: POST `/api/field-officer/visit/{id}/verify`
- Check geo-fence compliance rates
- Identify issues with multiple visits

### 4. **Analytics Dashboard**
Platform administrators:
- Track total visits across all issues
- Monitor geo-fence compliance
- Calculate average response times
- Identify high-activity officers

## Testing Recommendations

### Manual Testing

1. **Check-In Flow:**
   ```bash
   # Check in at an issue
   curl -X POST http://localhost:8000/api/field-officer/check-in \
     -H "Content-Type: application/json" \
     -d '{
       "issue_id": 1,
       "officer_email": "test@example.com",
       "officer_name": "Test Officer",
       "check_in_latitude": 19.0760,
       "check_in_longitude": 72.8777
     }'
   ```

2. **Upload Images:**
   ```bash
   curl -X POST http://localhost:8000/api/field-officer/visit/1/upload-images \
     -F "images=@photo1.jpg" \
     -F "images=@photo2.jpg"
   ```

3. **Check Out:**
   ```bash
   curl -X POST http://localhost:8000/api/field-officer/check-out \
     -H "Content-Type: application/json" \
     -d '{
       "visit_id": 1,
       "check_out_latitude": 19.0761,
       "check_out_longitude": 72.8778,
       "visit_duration_minutes": 30
     }'
   ```

4. **View History:**
   ```bash
   curl http://localhost:8000/api/field-officer/issue/1/visit-history
   ```

### Test Scenarios

1. **Within Geo-Fence:**
   - Check in within 100m of issue → `within_geofence: true`

2. **Outside Geo-Fence:**
   - Check in 200m away → `within_geofence: false`, distance recorded

3. **Invalid Coordinates:**
   - Latitude > 90 → 400 error
   - Longitude < -180 → 400 error

4. **Missing Issue:**
   - Check in to non-existent issue → 404 error

5. **Double Check-Out:**
   - Check out twice from same visit → 400 error

## Future Enhancements

1. **Real-Time Notifications:**
   - Alert citizens when officer checks in to their issue
   - Push notifications for check-in/check-out

2. **QR Code Verification:**
   - Generate QR codes at issue sites
   - Officers scan to verify location

3. **Offline Support:**
   - Cache check-ins when no network
   - Sync when connection restored

4. **Multi-Site Visits:**
   - Check in to multiple nearby issues in one visit
   - Batch visit creation

5. **Route Optimization:**
   - Suggest optimal visiting order for multiple issues
   - Integration with mapping services

6. **Automated Reporting:**
   - Weekly visit summary emails
   - Performance metrics per officer
   - Department-level analytics

## Dependencies

No new external dependencies required. Uses existing libraries:
- **FastAPI** - API framework
- **SQLAlchemy** - ORM and database
- **Pydantic** - Request/response validation
- **Python math** - Haversine distance calculation
- **hashlib** - SHA-256 hashing

## Files Modified/Created

### Created Files:
1. `backend/models.py` - Added `FieldOfficerVisit` model
2. `backend/schemas.py` - Added 7 check-in schemas
3. `backend/geofencing_service.py` - Geo-fencing logic (226 lines)
4. `backend/routers/field_officer.py` - API endpoints (500+ lines)
5. `FIELD_OFFICER_CHECKIN_FEATURE.md` - This documentation

### Modified Files:
1. `backend/init_db.py` - Added table migrations
2. `backend/main.py` - Registered field_officer router

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Search for "Field Officer Check-In" tag to see all endpoints with interactive testing.

## Conclusion

The Field Officer Check-In System provides:
- ✅ GPS-based location verification
- ✅ Public transparency of officer visits
- ✅ Immutable visit records (blockchain-style)
- ✅ Geo-fencing with configurable radius
- ✅ Visit documentation (notes + images)
- ✅ Analytics and compliance tracking
- ✅ Admin verification workflow

This feature enhances accountability, builds citizen trust, and provides data-driven insights into field operations.

---

**Implementation Date:** January 2024  
**Issue Reference:** [#288](https://github.com/RohanExploit/VishwaGuru/issues/288)  
**Status:** ✅ Complete
