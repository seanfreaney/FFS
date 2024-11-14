# FFS

I am a chartered accountant by current profession and qualified in 2022 under Chartered Accountants Ireland. Since then I have been working in finance in the Fin Tech industry but I have always toyed with the idea of starting my own business. This served as the inspiration for FFS - Freaney Financial Services.

My Goal was to create a website that would allow me to provide a range of services to potential clients. The initial offering would be preparation of monthly management accounts preparation however I would like to expand this to include other services in the future. In order to facilitate the process of providing these services, I needed to create a website that would allow me to simply share data with clients in a secure and efficient manner.

## Design

### Wire Frames

It was my intention to keep the design as simple as possible. Initially, 

- FFS Wireframes


## Models

### Home App

#### NewsletterSubscriber Model

Description:
Manages newsletter subscriptions by storing unique email addresses and subscription dates.

Fields:
1. email
   - Type: EmailField
   - Unique: True
   - Purpose: Stores subscriber's email address
   - Prevents duplicate subscriptions

2. date_added
   - Type: DateTimeField
   - Auto Now Add: True
   - Purpose: Automatically records subscription timestamp

String Representation:
Returns the subscriber's email address


### Profiles App

#### UserProfile Model

Description:
Extends the built-in Django User model to store additional user information and delivery details.

Fields:
1. user
   - Type: OneToOneField (User)
   - On Delete: CASCADE
   - Purpose: Links profile to Django User
   - Relationship: One-to-One

2. default_phone_number
   - Type: CharField
   - Max Length: 20
   - Null/Blank: True
   - Purpose: Stores contact number

3. default_country
   - Type: CountryField
   - Blank Label: 'Country *'
   - Null/Blank: True
   - Purpose: Stores country selection

4. default_postcode
   - Type: CharField
   - Max Length: 20
   - Null/Blank: True
   - Purpose: Stores postal code

5. default_town_or_city
   - Type: CharField
   - Max Length: 40
   - Null/Blank: True
   - Purpose: Stores town/city

6. default_street_address1
   - Type: CharField
   - Max Length: 80
   - Null/Blank: True
   - Purpose: Stores primary address

7. default_street_address2
   - Type: CharField
   - Max Length: 80
   - Null/Blank: True
   - Purpose: Stores secondary address

8. default_county
   - Type: CharField
   - Max Length: 80
   - Null/Blank: True
   - Purpose: Stores county/state

Special Functionality:
- Signal receiver automatically creates/updates profile when user is created
- All address fields are optional for flexibility

String Representation:
Returns the associated username


### Service Requests App

#### ServiceRequest Model

Description:
Core model handling business service requests, quotes, and payment processing.

Fields:
1. request_number
   - Type: UUIDField
   - Primary Key: True
   - Default: uuid.uuid4
   - Editable: False
   - Purpose: Unique identifier for requests

2. user
   - Type: ForeignKey (User)
   - On Delete: CASCADE
   - Purpose: Links request to user

3. business_type
   - Type: CharField
   - Max Length: 100
   - Purpose: Stores business category

4. monthly_revenue
   - Type: DecimalField
   - Max Digits: 10
   - Decimal Places: 2
   - Purpose: Stores monthly revenue figures

5. monthly_transactions
   - Type: IntegerField
   - Purpose: Stores transaction count

6. monthly_operating_costs
   - Type: DecimalField
   - Max Digits: 10
   - Decimal Places: 2
   - Purpose: Stores operating costs

7. quote_amount
   - Type: DecimalField
   - Max Digits: 10
   - Decimal Places: 2
   - Null/Blank: True
   - Purpose: Stores service quote amount

8. quote_accepted
   - Type: BooleanField
   - Default: False
   - Purpose: Tracks quote acceptance

9. status
   - Type: CharField
   - Max Length: 20
   - Choices: STATUS_CHOICES
   - Purpose: Tracks request status

10. quote_status
    - Type: CharField
    - Max Length: 20
    - Choices: QUOTE_STATUS_CHOICES
    - Default: 'pending'
    - Purpose: Tracks quote status

11. created_on
    - Type: DateTimeField
    - Auto Now Add: True
    - Purpose: Records creation timestamp

12. stripe_payment_intent_id
    - Type: CharField
    - Max Length: 255
    - Null/Blank: True
    - Purpose: Stores Stripe payment ID

13. is_paid
    - Type: BooleanField
    - Default: False
    - Purpose: Tracks payment status

Special Functionality:
- mark_as_paid() method updates payment status and request status


#### Document Model

Description:
Manages document uploads and storage for service requests.

Fields:
1. service_request
   - Type: ForeignKey (ServiceRequest)
   - On Delete: CASCADE
   - Related Name: 'documents'
   - Purpose: Links document to service request

2. file
   - Type: FileField
   - Upload To: 'documents/'
   - Purpose: Stores uploaded file

3. is_bank_statement
   - Type: BooleanField
   - Default: True
   - Purpose: Identifies bank statements

4. uploaded_at
   - Type: DateTimeField
   - Auto Now Add: True
   - Purpose: Records upload timestamp

5. uploaded_by
   - Type: ForeignKey (User)
   - On Delete: SET_NULL
   - Null/Blank: True
   - Purpose: Tracks who uploaded document

6. document_type
   - Type: CharField
   - Max Length: 20
   - Choices: DOCUMENT_TYPE_CHOICES
   - Default: 'customer'
   - Purpose: Categorizes document type

Special Functionality:
- Automatically deletes old file when updated
- Custom save method handles file replacement

String Representation:
Returns document identifier with request number

## Model Relationships

### User Model (Django Built-in) Relationships

Django User Model is the central model with connections to:

1. UserProfile (One-to-One)
   - Each User has exactly one UserProfile
   - Created automatically via signal when User is created
   - Relationship defined in UserProfile model:
     user = models.OneToOneField(User, on_delete=models.CASCADE)

2. ServiceRequest (One-to-Many)
   - One User can have many ServiceRequests
   - Relationship defined in ServiceRequest model:
     user = models.ForeignKey(User, on_delete=models.CASCADE)

3. Document (One-to-Many)
   - One User can upload many Documents
   - Tracks document uploader
   - Relationship defined in Document model:
     uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL)


### ServiceRequest Model Relationships

ServiceRequest connects to:

1. User (Many-to-One)
   - Many ServiceRequests can belong to one User
   - Deleting a User deletes all their ServiceRequests (CASCADE)

2. Document (One-to-Many)
   - One ServiceRequest can have multiple Documents
   - Relationship defined in Document model:
     service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
   - Accessible via 'documents' related name:
     service_request.documents.all()


### Document Model Relationships

Document connects to:

1. ServiceRequest (Many-to-One)
   - Many Documents can belong to one ServiceRequest
   - Deleting a ServiceRequest deletes all associated Documents (CASCADE)

2. User (Many-to-One)
   - Many Documents can be uploaded by one User
   - If User is deleted, uploaded_by becomes NULL (SET_NULL)


### NewsletterSubscriber Model

- Standalone model with no relationships to other models
- Stores unique email addresses independently


### Key Points:
1. Deletion Behavior:
   - Deleting a User cascades to delete their Profile and ServiceRequests
   - Deleting a ServiceRequest cascades to delete its Documents
   - Deleting a User nullifies their Document uploads rather than deleting them

2. Access Patterns:
   - User → Profile: user.userprofile
   - User → ServiceRequests: user.servicerequest_set.all()
   - ServiceRequest → Documents: service_request.documents.all()
   - Document → ServiceRequest: document.service_request
   - Document → Uploader: document.uploaded_by


## Templates/Functionality

### Base.html
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

### Custom 404.html
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



## E-Commerce Functionality

### Initial Setup and DOM Checks

```javascript
document.addEventListener('DOMContentLoaded', function() {
const paymentForm = document.getElementById('payment-form');
const cardElement = document.getElementById('card-element');
if (paymentForm && cardElement) {
console.log('Stripe Public Key:', stripePublicKey);
```

This section:
- Ensures DOM is fully loaded before initialization
- Checks for payment form elements
- Validates required Stripe keys are present

### Stripe Elements Configuration

```javascript
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();
const card = elements.create('card');
card.mount('#card-element');
```

This section:
- Configures Stripe elements
- Creates card element
- Mounts card element to the DOM

### Real-time Card Validation

```javascript
card.on('change', function(event) {
const displayError = document.getElementById('card-errors');
if (event.error) {
displayError.textContent = event.error.message;
} else {
displayError.textContent = '';
}
});
```

Provides:
- Instant feedback on card input
- Validation for:
  - Card number format
  - Expiry date validity
  - CVC format
  - Card type recognition
- Real-time error messages

### Payment Form Submission

```javascript
paymentForm.addEventListener('submit', async function(e) {
e.preventDefault();
paymentButton.disabled = true;
try {
// Create Payment Intent
const response = await fetch(createPaymentIntentUrl, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'X-CSRFToken': csrfToken
}
});
const data = await response.json();
if (data.error) {
handleError(data.error);
return;
}
// Confirm Payment
const { error, paymentIntent } = await stripe.confirmCardPayment(
data.clientSecret,
{
payment_method: { card: card }
}
);
```

Handles:
- Form submission prevention
- Double-submission protection
- Payment Intent creation
- CSRF protection
- Error catching and handling

### Comprehensive Error Handling

```javascript
if (error) {
console.error('Payment error:', error);
const errorDiv = document.getElementById('card-errors');
errorDiv.textContent = error.message;
errorDiv.classList.add('alert', 'alert-danger');
paymentButton.disabled = false;
} else {
if (paymentIntent.status === 'succeeded') {
handleSuccess(data.requestNumber);
} else {
handleUnexpectedStatus(paymentIntent.status);
}
}
```

Manages:
- Card processing errors
- Network failures
- Server response errors
- Unexpected payment states
- User feedback display



## Authentication


## Business Model / Marketing Strategy

### Business Model

### Facebook mockup


## Unfixed Bugs

## Additional Features



# Testing


### Manual Testing Table

| Action    | Expectation | Result | 
| ---------|:-------------------:|----------|
| Click 'Home' link | directed to Index.html | Pass |

## Automated Tests Documentation

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


## Deployment