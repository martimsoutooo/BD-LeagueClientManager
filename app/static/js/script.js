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
                                <p class="card-text mb-0" style="font-size: small;">Price: ${champion.BE_Price} BE</p>
                                <button class="btn btn-primary" onclick="buyChampion('${champion.ID_Item_Type}', '${champion.BE_Price}')">Buy</button>
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
    fetch('/buy_champion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ champion_id: championId, be_price: bePrice })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    });
}
