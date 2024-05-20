document.addEventListener('DOMContentLoaded', function () {
    const alphabeticalFilter = document.getElementById('alphabeticalFilter');
    const kingdomFilter = document.getElementById('kingdomFilter');
    const categoryFilter = document.getElementById('categoryFilter');

    setFiltersFromUrl();

    alphabeticalFilter.addEventListener('change', applyFilters);
    kingdomFilter.addEventListener('change', applyFilters);
    categoryFilter.addEventListener('change', applyFilters);

    function applyFilters() {
        const isAlphabetical = alphabeticalFilter.checked ? 1 : 0;
        const selectedKingdom = kingdomFilter.value;
        const selectedCategory = categoryFilter.value;

        console.log('Filters applied:', { isAlphabetical, selectedKingdom, selectedCategory });

        const params = new URLSearchParams({
            alphabetical: isAlphabetical,
            kingdom: selectedKingdom,
            category: selectedCategory
        });

        fetch(`/filter_champions?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateChampionList(data.champions);
                } else {
                    console.error('Error fetching filtered data:', data.message);
                }
            });
    }

    function setFiltersFromUrl() {
        const params = new URLSearchParams(window.location.search);
        const isAlphabetical = params.get('alphabetical') === '1';
        const selectedKingdom = params.get('kingdom') || 'all';
        const selectedCategory = params.get('category') || 'all';

        alphabeticalFilter.checked = isAlphabetical;
        kingdomFilter.value = selectedKingdom;
        categoryFilter.value = selectedCategory;

        applyFilters();
    }

    function updateChampionList(champions) {
        const championContainer = document.querySelector('.scrollable-content2');
        championContainer.innerHTML = '';

        champions.forEach(champion => {
            const championCard = `
                <div class="col-md-4">
                    <div class="card mb-3 shadow-sm">
                        <div class="card-body d-flex flex-column justify-content-between">
                            <div>
                                <h5 class="card-title font-weight-bold">${champion.Name}</h5>
                                <p class="card-text" style="margin-bottom: 0.2rem;">Category: ${champion.Category}</p>
                                <p class="card-text" style="margin-bottom: 1rem;">Kingdom: ${champion.Kingdom}</p>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <p class="card-text mb-0" style="font-size: small;">Price: ${champion.BE_Price} <img src="https://server.blix.gg/imgproxy/nP7l6vA2EI8fTz4xs51FwU7acvVmJx2yR-Fo_iUmeHI/rs:fit:260:260:0/g:no/aHR0cDovL21pbmlvOjkwMDAvaW1hZ2VzLzQxM2I0ZTQzNzFjYjQxYTliMzQwNDJhNTBmNDg4NjVhLnBuZw.webp"
                                alt="" class="stats-image"></p>
                                <button class="btn btn-primary" onclick="buyChampion('${champion.ID}', '${champion.BE_Price}')">Buy</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            championContainer.innerHTML += championCard;
        });
    }
});

function buyChampion(championId, bePrice) {
    console.log("Attempting to buy champion with ID:", championId, "and BE Price:", bePrice);
    fetch('/buy_champion_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ champion_id: championId, be_price: bePrice })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response data:", data);
        alert(data.message);
        if (data.status === 'success') {
            location.reload();  // Recarrega a página após compra bem-sucedida
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
        alert("An error occurred while processing your request.");
    });
}

function buySkin(skinId, rpPrice) {
    console.log("Attempting to buy skin with ID:", skinId, "and RP Price:", rpPrice);
    fetch('/buy_skin_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skin_id: skinId, rp_price: rpPrice })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response data:", data);
        alert(data.message);
        if (data.status === 'success') {
            location.reload();  // Recarrega a página após compra bem-sucedida
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
        alert("An error occurred while processing your request.");
    });
}

document.getElementById("logoutButton").addEventListener("click", function() {
    fetch('/logout')
        .then(response => {
            if (response.ok) {
                window.location.href = '/login';
            } else {
                alert('Logout failed');
            }
        });
});

function purchaseRP() {
    const rpAmount = document.getElementById('rpAmount').value;

    fetch('/purchase_rp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rp_amount: rpAmount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const checkboxInputs = document.querySelectorAll('.checkbox-input');

    checkboxInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (this.checked) {
                console.log('Checked:', this.id);
            } else {
                console.log('Unchecked:', this.id);
            }
        });
    });
});

function buyWard(wardId, rpPrice) {
    console.log("Attempting to buy ward with ID:", wardId, "and RP Price:", rpPrice);
    fetch('/buy_ward_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ward_id: wardId, rp_price: rpPrice })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response data:", data);
        alert(data.message);
        if (data.status === 'success') {
            location.reload();  // Recarrega a página após compra bem-sucedida
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
        alert("An error occurred while processing your request.");
    });
}

function buyChest(chestId, rpPrice) {
    console.log("Attempting to buy chest with ID:", chestId, "and RP Price:", rpPrice);
    fetch('/buy_chest_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chest_id: chestId, rp_price: rpPrice })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response data:", data);
        alert(data.message);
        if (data.status === 'success') {
            location.reload();  // Recarrega a página após compra bem-sucedida
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
        alert("An error occurred while processing your request.");
    });
}











