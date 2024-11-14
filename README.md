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

# Automated Tests Documentation

## Profile Tests

### Forms (profiles/tests/test_forms.py)

### test_form_fields_are_explicit_in_form_metaclass
```Test that the correct fields are excluded in the form```
- Validates form metaclass configuration
- Ensures 'user' field is properly excluded

### test_form_fields_are_present
```Test that the expected fields are present in the form```
- Verifies presence of all required profile fields
- Validates all address and contact fields exist

### Views (profiles/tests/test_views.py)

### test_profile_view_redirect_if_not_logged_in
```Test profile view redirects if user is not logged in```
- Verifies unauthorized access handling
- Confirms redirect to login page

### test_profile_view_GET
```Test GET request to profile view```
- Validates successful profile page load
- Verifies correct template usage
- Confirms presence of form and service requests in context

### test_profile_view_POST_valid_data
```Test POST request with valid form data```
- Tests profile update functionality
- Verifies successful data submission
- Confirms success message display

### test_profile_view_displays_service_requests
```Test that service requests are displayed in profile```
- Validates service request display
- Verifies correct user-request association

### test_profile_view_POST_invalid_data
```Test POST request with invalid form data```
- Tests form validation for invalid input
- Verifies error handling for invalid data

### test_profile_view_POST_empty_data
```Test POST request with empty data```
- Validates handling of empty form submission
- Confirms optional field behavior

### test_service_requests_ordered_by_created_on
```Test that service requests are displayed in correct order```
- Verifies chronological ordering
- Confirms newest-first sorting

### test_on_profile_page_context
```Test that on_profile_page context is True```
- Validates context variable setting
- Verifies page identification

### test_profile_view_with_no_service_requests
```Test profile view when user has no service requests```
- Tests empty state handling
- Verifies correct display with no requests

### Models (profiles/tests/test_models.py)

### test_profile_str_method
```Test the string representation of the UserProfile model```
- Validates profile string representation
- Verifies username display

### test_profile_created_on_user_creation
```Test that a UserProfile is automatically created when a User is created```
- Confirms automatic profile creation
- Verifies user-profile relationship

### test_profile_fields_are_optional
```Test that all profile fields except user are optional```
- Validates optional field configuration
- Verifies default values for all fields

## Service Request Tests

### Forms (service_requests/tests/test_forms.py)

### test_service_request_form_valid_data
```Test form with valid data```
- Validates form processing with correct data
- Verifies successful form validation

### test_service_request_form_invalid_data
```Test form with missing required fields```
- Tests form validation with invalid data
- Verifies error handling for missing fields
- Validates decimal field validation

### test_document_form_valid_data
```Test document form with valid file```
- Validates file upload functionality
- Verifies form processing with valid PDF

### test_document_form_invalid_file_type
```Test document form with invalid file type```
- Tests file type validation
- Verifies rejection of invalid file types

### Views (service_requests/tests/test_views.py)

### test_create_service_request_get
```Test GET request for service request creation```
- Validates form display
- Verifies template usage

### test_create_service_request_post
```Test POST request for service request creation```
- Tests request creation with valid data
- Verifies file upload handling
- Confirms successful submission

### test_service_request_detail
```Test service request detail view```
- Validates detail page display
- Verifies correct context data

### test_service_request_list
```Test service request listing```
- Tests request list display
- Verifies correct template usage
- Validates context data

### test_edit_service_request
```Test service request editing```
- Validates update functionality
- Verifies data persistence
- Tests redirect behavior

### test_quote_response
```Test quote response handling```
- Tests quote status updates
- Verifies response processing

### test_delete_service_request
```Test service request deletion```
- Validates deletion functionality
- Verifies proper cleanup

### test_edit_service_request_unauthorized
```Test unauthorized edit attempts```
- Validates access control
- Verifies 404 response for unauthorized users

### test_quote_response_invalid_status
```Test invalid quote response handling```
- Tests invalid status validation
- Verifies status remains unchanged

### test_delete_service_request_unauthorized
```Test unauthorized deletion attempts```
- Validates deletion restrictions
- Verifies redirect behavior

### test_views_require_login
```Test login requirements for views```
- Validates authentication requirements
- Verifies redirect to login

### test_edit_nonexistent_service_request
```Test editing non-existent requests```
- Validates 404 response
- Tests error handling

### test_quote_response_already_processed
```Test quote response for processed quotes```
- Validates quote status protection
- Verifies unchanged status

### test_create_service_request_invalid_data
```Test invalid service request creation```
- Tests form validation
- Verifies error handling
- Validates file type restrictions

### test_edit_service_request_invalid_data
```Test invalid service request editing```
- Tests form validation during edit
- Verifies error handling
- Validates context data

### test_service_request_list_empty
```Test empty service request list```
- Validates empty state handling
- Verifies zero-request display

### test_service_request_detail_context
```Test detail view context```
- Validates context data
- Verifies Stripe key presence

### test_delete_service_request_get
```Test delete confirmation page```
- Validates confirmation template
- Tests GET request handling

### test_delete_service_request_staff
```Test staff deletion privileges```
- Validates staff permissions
- Verifies successful deletion

### test_edit_service_request_get
```Test edit form display```
- Validates form context
- Verifies template usage

### test_create_service_request_invalid_document
```Test invalid document upload```
- Tests document validation
- Verifies error handling


## Service Request Models Tests (service_requests/tests/test_models.py)

### test_mark_as_paid
```Test mark_as_paid method updates status correctly```
- Validates payment status update
- Verifies status change to 'in_progress'

### test_document_str_representation
```Test the string representation of Document```
- Validates document string format
- Verifies request number inclusion

### test_document_file_update
```Test that old file is deleted when updating document```
- Tests file replacement functionality
- Verifies old file deletion
- Validates new file storage

## Payment Tests (service_requests/tests/test_payment_views.py)

### test_create_payment_intent_success
```Test successful payment intent creation```
- Validates Stripe API integration
- Verifies client secret generation
- Tests metadata handling

### test_create_payment_intent_unauthorized
```Test unauthorized payment intent creation```
- Validates authentication requirements
- Verifies redirect to login

### test_create_payment_intent_invalid_request
```Test payment intent creation with invalid requests```
- Tests validation of quote status
- Verifies error handling for invalid requests

### test_payment_success_view
```Test the payment success view```
- Validates success redirect
- Verifies detail page navigation

### test_check_payment_status
```Test the payment status check endpoint```
- Tests payment status tracking
- Validates JSON response format
- Verifies status updates

### test_create_payment_intent_wrong_user
```Test creating payment intent for another user's request```
- Validates user authorization
- Verifies access control

### test_payment_success_not_paid
```Test payment success view when payment is not confirmed```
- Tests pending payment handling
- Verifies message display

### test_payment_success_already_paid
```Test payment success view for confirmed payments```
- Validates paid status handling
- Verifies success message

### test_check_payment_status_unauthorized
```Test check payment status with wrong user```
- Tests unauthorized access handling
- Verifies 404 response

### test_check_payment_status_nonexistent
```Test check payment status with non-existent request```
- Validates non-existent request handling
- Verifies error response

### test_create_payment_intent_stripe_error
```Test handling of Stripe API errors```
- Tests Stripe error handling
- Validates error response format

### test_payment_success_invalid_request
```Test payment success view with invalid request number```
- Tests non-existent request handling
- Verifies 404 response

## Management Tests (management/tests/test_views.py)

### test_management_dashboard_view
```Test access control for management dashboard```
- Validates staff-only access
- Tests redirect for non-staff users
- Verifies successful access for staff
- Confirms correct template usage

### test_service_request_management_view
```Test service request management functionality```
- Validates request listing display
- Tests status filtering functionality
- Verifies staff-only access
- Confirms correct template usage
- Tests request count accuracy

### test_service_request_detail_view
```Test service request detail functionality```
- Validates detail view access control
- Tests context data accuracy
- Verifies staff-only access
- Confirms request data display

### test_upload_owner_document_view
```Test document upload functionality```
- Validates file upload process
- Tests access control for uploads
- Verifies successful file storage
- Confirms error handling for invalid uploads

### test_service_request_detail_post
```Test service request update functionality```
- Validates status update process
- Tests quote amount modifications
- Verifies data persistence
- Confirms validation handling

### test_management_dashboard_counts
```Test dashboard statistics accuracy```
- Validates request counting by status
- Tests pending request count
- Verifies in-progress request count
- Confirms completed request count

### test_service_request_management_date_ordering
```Test date-based request ordering```
- Validates chronological sorting
- Tests newest-first ordering
- Verifies oldest-first ordering
- Confirms sort preference handling

### test_success_messages
```Test system feedback messages```
- Validates success message display
- Tests message content accuracy
- Verifies message integration

### test_document_upload_validation
```Test document upload validation```
- Validates file type restrictions
- Tests file size limits
- Verifies successful upload process
- Confirms error handling