function validateLogin() {
    window.location.href = "index.html"; // directly redirect to home page
}
function applyCustomization() {
    alert("Customization applied!");
}

function showBuySection() {
    document.getElementById("buySection").classList.remove("hidden");
    document.getElementById("sellSection").classList.add("hidden");
}

function showSellSection() {
    document.getElementById("sellSection").classList.remove("hidden");
    document.getElementById("buySection").classList.add("hidden");
}
function searchProperties() {
    const budget = document.getElementById("budget").value;
    document.getElementById("buyResults").innerHTML = `Displaying properties under ₹${budget}.`;
}

function submitListing() {
    const sellerName = document.getElementById("sellerName").value;
    const sellerPhone = document.getElementById("sellerPhone").value;
    const sellPrice = document.getElementById("sellPrice").value;
    document.getElementById("sellSection").innerHTML = 
        `<p>Thank you, ${sellerName}. Your listing at ₹${sellPrice} has been submitted!</p>`;
}


function listHome() {
    alert("Your home has been listed!");
}
// Preview Image Upload
function previewImage(event) {
    const imagePreview = document.getElementById("imagePreview");
    imagePreview.innerHTML = ""; // Clear previous image
    
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.alt = "Dream House Image";
            img.style.maxWidth = "100%";
            img.style.height = "auto";
            imagePreview.appendChild(img);
        };
        reader.readAsDataURL(file);
    }
}

// Show Preview of Description and Image
function showPreview() {
    const description = document.getElementById("houseDescription").value;
    const descriptionPreview = document.getElementById("descriptionPreview");
    descriptionPreview.textContent = description ? `Description: ${description}` : "No description provided.";
}

// Reset Design
function resetDesign() {
    document.getElementById("houseImage").value = "";
    document.getElementById("houseDescription").value = "";
    document.getElementById("imagePreview").innerHTML = "";
    document.getElementById("descriptionPreview").textContent = "Preview will appear here.";
}
// Show the Sell form
function showRentOrBuy(option) {
    document.getElementById("rentSection").style.display = option === 'rent' ? 'block' : 'none';
    document.getElementById("buySection").style.display = option === 'buy' ? 'block' : 'none';
}

// Rent Section
function showRent(option) {
    document.getElementById("rentForm").style.display = option === 'rent' ? 'block' : 'none';
    document.getElementById("rentSellForm").style.display = option === 'sell' ? 'block' : 'none';
}

// Buy Section
function showBuy(option) {
    document.getElementById("buyForm").style.display = option === 'buy' ? 'block' : 'none';
    document.getElementById("buySellForm").style.display = option === 'sell' ? 'block' : 'none';
}

// Show rental listings based on rent budget
function showRentListings() {
    const rentBudget = document.getElementById("rentBudget").value;
    const rentResults = document.getElementById("rentResults");

    if (rentBudget) {
        const rentals = [
            { rent: 150000, description: "2 BHK in city center" },
            { rent: 100000, description: "1 BHK near metro" },
            { rent: 75000, description: "2 BHK in suburbs" },
            { rent: 50000, description: "Studio in rural area" }
        ];
        const filteredRentals = rentals.filter(rental => rental.rent <= rentBudget);
        rentResults.innerHTML = filteredRentals.length
            ? filteredRentals.map(rental => `<div class="listing"><strong>Annual Rent:</strong> ₹${rental.rent}<br><strong>Description:</strong> ${rental.description}</div>`).join('')
            : "<p>No rental listings available.</p>";
    } else {
        alert("Enter your annual rent budget.");
    }
}

// Show buy listings based on budget and area
function showBuyListings() {
    const buyBudget = document.getElementById("buyBudget").value;
    const areaType = document.getElementById("areaType").value;
    const buyResults = document.getElementById("buyResults");

    if (buyBudget && areaType) {
        const properties = [
            { price: 500000, description: "Modern city center apartment", area: "Urban" },
            { price: 750000, description: "House with garden", area: "Urban" },
            { price: 300000, description: "Cozy rural cottage", area: "Rural" },
            { price: 450000, description: "Farmhouse with land", area: "Rural" }
        ];
        const filteredProperties = properties.filter(property => property.price <= buyBudget && property.area === areaType);
        buyResults.innerHTML = filteredProperties.length
            ? filteredProperties.map(property => `<div class="listing"><strong>Price:</strong> ₹${property.price}<br><strong>Description:</strong> ${property.description}</div>`).join('')
            : "<p>No properties available.</p>";
    } else {
        alert("Enter budget and area type.");
    }
}

// Submit sell listing
function submitSellListing(section) {
    alert(`Listing submitted for ${section} section.`);
}console.log(result); // Check the response object
async function loginUser(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Simulate a successful login
    if (username === "test" && password === "1234") { // Replace with expected credentials for testing
        alert("Login successful");
        localStorage.setItem('token', "fake-token"); // Simulate a token
        window.location.href = "index.html"; // Change to the correct main page
    } else {
        alert("Login failed: Incorrect username or password");
    }
}






