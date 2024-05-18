document.addEventListener('DOMContentLoaded', function () {
    const alphabeticalFilter = document.getElementById('alphabeticalFilter');
    const kingdomFilter = document.getElementById('kingdomFilter');
    const categoryFilter = document.getElementById('categoryFilter');

    // Set filters based on URL parameters
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

        applyFilters();  // Fetch initial data based on URL parameters
    }

    function updateChampionList(champions) {
        const championContainer = document.querySelector('.scrollable-content');
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
    console.log("Attempting to buy champion with ID:", championId, "and BE Price:", bePrice); // Log para depuração
    fetch('/buy_champion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ champion_id: championId, be_price: bePrice })
    })
    .then(response => {
        console.log("Response status:", response.status); // Log para depuração
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data); // Log para depuração
        if (data.status === 'success') {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error); // Log para depuração
    });
}

function buySkin(skinId, rpPrice) {
    console.log("Attempting to buy skin with ID:", skinId, "and RP Price:", rpPrice); // Log para depuração
    fetch('/buy_skin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skin_id: skinId, rp_price: rpPrice })  // Correção aqui
    })
    .then(response => {
        console.log("Response status:", response.status); // Log para depuração
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data); // Log para depuração
        if (data.status === 'success') {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error); // Log para depuração
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
                // Do something when the checkbox is checked
                console.log('Checked:', this.id);
            } else {
                // Do something when the checkbox is unchecked
                console.log('Unchecked:', this.id);
            }
        });
    });
});







