function updatePrice(price) {
        alert('Total Cost: $' + price);
    }
 function updatePrice(price) {
            document.getElementById("price").innerText = "$" + price;
            document.getElementById("hiddenPrice").value = price;
        }

function updatePrice(val) {
    document.getElementById('price').textContent = '$' + val;
    document.getElementById('hiddenPrice').value = val;
}
// Update price display when service changes
function updatePrice(val) {
    const priceDisplay = document.getElementById('service-price');
    const hiddenPrice = document.getElementById('hiddenPrice');
    if (priceDisplay) priceDisplay.textContent = "Price: $" + val;
    if (hiddenPrice) hiddenPrice.value = val;
}

// Set initial price on page load
document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('service-select') || document.getElementById('service');
    if (serviceSelect) {
        updatePrice(serviceSelect.value);
        serviceSelect.addEventListener('change', function() {
            updatePrice(this.value);
        });
    }

    // AJAX form submission for appointment booking
    const appointmentForm = document.getElementById('appointment-form');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(appointmentForm);
            const data = {};
            formData.forEach((value, key) => { data[key] = value; });

            fetch(appointmentForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Appointment booked!');
                    // Optionally refresh appointments list
                    fetchAppointments();
                } else {
                    alert(result.error || 'Failed to book appointment.');
                }
            })
            .catch(() => alert('Error submitting appointment.'));
        });
    }

    // Function to fetch and display appointments (example)
    function fetchAppointments() {
        fetch('/auth/my_appointments', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById('appointments-list');
                if (list && Array.isArray(data.appointments)) {
                    list.innerHTML = '';
                    data.appointments.forEach(appt => {
                        const li = document.createElement('li');
                        li.textContent = `${appt.date} at ${appt.time} — ${appt.service} ($${appt.price})`;
                        list.appendChild(li);
                    });
                }
            });
    }
});
