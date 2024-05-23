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

function buyWard(wardId, rpPrice) {
    console.log("Attempting to buy ward with ID:", wardId, "and RP Price:", rpPrice);
    fetch('/buy_ward_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ward_id: wardId, rp_price: rpPrice })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
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



















