// Initialize Stripe
const stripe = Stripe(stripePublicKey);

// Create an instance of Elements
const elements = stripe.elements();

// Create the card Element
const card = elements.create('card');

document.addEventListener('DOMContentLoaded', function() {
    // Mount the card Element
    card.mount('#card-element');
    
    const paymentButton = document.getElementById('payment-button');
    const paymentForm = document.getElementById('payment-form');
    
    if (paymentForm) {
        paymentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Disable the button to prevent double clicks
            paymentButton.disabled = true;
            
            try {
                // Create the payment intent
                const response = await fetch(createPaymentIntentUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    }
                });
                
                const data = await response.json();
                
                if (data.error) {
                    console.error('Error:', data.error);
                    paymentButton.disabled = false;
                    return;
                }
                
                // Confirm the card payment
                const { error, paymentIntent } = await stripe.confirmCardPayment(
                    data.clientSecret,
                    {
                        payment_method: {
                            card: card,
                        }
                    }
                );
                
                if (error) {
                    console.error('Payment error:', error);
                    const errorDiv = document.getElementById('card-errors');
                    errorDiv.textContent = error.message;
                    errorDiv.classList.add('alert', 'alert-danger');
                    paymentButton.disabled = false;
                } else {
                    if (paymentIntent.status === 'succeeded') {
                        // Show processing message
                        const messageDiv = document.getElementById('card-errors');
                        messageDiv.textContent = 'Payment received! Processing your request...';
                        messageDiv.classList.remove('alert-danger');
                        messageDiv.classList.add('alert', 'alert-info');
                        
                        // Redirect to success page and force refresh
                        window.location.href = `/service-requests/${data.requestNumber}/payment-success/`;
                        
                        // Add a small delay and refresh
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    } else {
                        console.error('Unexpected payment status:', paymentIntent.status);
                        const messageDiv = document.getElementById('card-errors');
                        messageDiv.textContent = 'Something went wrong. Please try again or contact support.';
                        messageDiv.classList.add('alert', 'alert-danger');
                        paymentButton.disabled = false;
                    }
                }
                
            } catch (error) {
                console.error('Error:', error);
                paymentButton.disabled = false;
            }
        });
    }
    
    // Handle real-time validation errors from the card Element
    card.on('change', function(event) {
        const displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
});