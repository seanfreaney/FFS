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