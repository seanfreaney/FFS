// Add debug logs
console.log('Stripe Public Key:', stripePublicKey);
console.log('CSRF Token:', csrfToken);
console.log('Payment Intent URL:', createPaymentIntentUrl);

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
                    document.getElementById('card-errors').textContent = error.message;
                    paymentButton.disabled = false;
                } else {
                    if (paymentIntent.status === 'succeeded') {
                        // Payment successful - redirect to success page
                        window.location.href = `/service-requests/${data.requestNumber}/payment-success/`;
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