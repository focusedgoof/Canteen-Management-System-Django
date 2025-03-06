document.getElementById('add-item-btn').addEventListener('click', function() {
    var container = document.getElementById('item-container');
    var newRow = document.createElement('div');
    newRow.classList.add('item-row');
    newRow.innerHTML = `
        <label for="items">Select Item:</label>
        <select name="items" class="item-select" required>
            {% for item in items %}
                <option value="{{ item.id }}">{{ item.ItemName }} - Rs.{{ item.Amount }}</option>
            {% endfor %}
        </select>
        
        <label for="quantity">Quantity:</label>
        <input type="number" name="quantity" class="item-quantity" min="1" required>
        
        <button type="button" class="remove-item-btn">Remove Item</button>
    `;
    container.appendChild(newRow);

    // Add event listener to the remove button for this new row
    newRow.querySelector('.remove-item-btn').addEventListener('click', function() {
        container.removeChild(newRow);
    });
});

// Add event listeners to existing remove buttons
document.querySelectorAll('.remove-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        button.parentElement.remove();
    });
});