# FFS

I am a chartered accountant by current profession and qualified in 2022 under Chartered Accountants Ireland. Since then I have been working in finance in the Fin Tech industry but I have always toyed with the idea of starting my own business. This served as the inspiration for FFS - Freaney Financial Services.

My Goal was to create a website that would allow me to provide a range of services to potential clients. The initial offering would be preparation of monthly management accounts preparation however I would like to expand this to include other services in the future. In order to facilitate the process of providing these services, I needed to create a website that would allow me to simply share data with clients in a secure and efficient manner.

## Design

### Wire Frames

It was my intention to keep the design as simple as possible. Initially, 

- FFS Wireframes


## Features

- Base.html
 - Navbar
  - fixed position header with dark theme
  - conditional rendering of links based on user authentication status
  - links to Home, Management, Profiles, Service Requests and Sign In/Register
  - hamburger menu for authenticated users for better user experience

 - Messages
  - Django messages framework used to provide feedback to users

 - Footer
  - fixed position footer with dark theme
  - copyright information (for the purpose of the project)
  - social media links with accessibility attributes

- 404.html
 - extends base.html
 - 404 error page with simple explanation
 - return to homepage button

### Home App

- Index.html    
 - Main section
  - hero section with main heading and tagline
  - about us card with company introduction and three core principles
  - services card with brief introduction to the services offered
  - call to action button to request services
  - newsletter signup form for webmarketing

### Management

- management_dashboard.html

- service_request_detail.html

- service_request_management.html

### Profiles

- Profile.html

### Service_Requests

- create_service_request.html

- edit_service_request.html

- service_request_list.html

- service_request_detail.html

- request_confirm_delete.html


## Business Model / Marketing Strategy


### Manual Testing Table

| Action    | Expectation | Result | 
| ---------|:-------------------:|----------|
| Click 'Home' link | directed to Recipe List | Pass |

## Automated Tests

The following automated tests are implemented in the management views test suite:

### Access Control and Dashboard Tests
```python
test_management_dashboard_view
```
- Validates dashboard access control mechanisms
- Ensures non-staff users are properly redirected
- Verifies staff users can access dashboard
- Confirms correct template rendering

### Service Request Management Tests
```python
test_service_request_management_view
```
- Tests service request listing functionality
- Validates access control for staff/non-staff users
- Verifies request filtering by status
- Ensures proper display of service requests

```python
test_service_request_detail_view
```
- Tests individual service request detail views
- Validates access restrictions
- Verifies correct context data provision
- Tests staff access permissions

### Document Management Tests
```python
test_upload_owner_document_view
```
- Validates document upload functionality
- Tests access control for uploads
- Verifies successful file upload scenarios
- Tests handling of missing file submissions

### Data Manipulation Tests
```python
test_service_request_detail_post
```
- Tests service request update functionality
- Validates status updates
- Verifies quote amount modifications
- Tests invalid input handling

### Dashboard Statistics Tests
```python
test_management_dashboard_counts
```
- Validates dashboard statistics accuracy
- Tests request counting by status
- Verifies correct statistical displays
- Ensures accurate data representation

### Sorting and Ordering Tests
```python
test_service_request_management_date_ordering
```
- Tests date-based request sorting
- Validates newest-first ordering
- Verifies oldest-first ordering
- Ensures correct sequence maintenance

### User Feedback Tests
```python
test_success_messages
```
- Validates system feedback mechanisms
- Tests success message display
- Verifies user notification functionality

### File Upload Validation Tests
```python
test_document_upload_validation
```
- Tests document upload validation
- Verifies file upload functionality
- Validates successful upload scenarios
- Tests post-upload redirects


