const BASE_URL = "http://localhost:5000/api";

function createCupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor}
        </li>
          
        <li>
          ${cupcake.size}
        </li>
           
        <li>
          ${cupcake.rating}  
        </li>

        <li>
          <button class="delete-button">Delete Cupcake</button>
        </li>
        <img class="Cupcake-img" src="${cupcake.image}">
      </div>`
      ;
  }

async function showInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    const data = response.data;
    
    const cupcakesList = document.getElementById("cupcakes-list");
    data.cupcakes.forEach(cupcakeData => {
        const newCupcake = createCupcakeHTML(cupcakeData);
        cupcakesList.insertAdjacentHTML("beforeend", newCupcake);
    });
}
  
  // Function to handle form submission for adding new cupcakes
document.getElementById("new-cupcake-form").addEventListener("submit", async function (evt) {
    evt.preventDefault();
  
    const flavor = document.getElementById("form-flavor").value;
    const rating = document.getElementById("form-rating").value;
    const size = document.getElementById("form-size").value;
    const image = document.getElementById("form-image").value;
  
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
  
    const newCupcakeData = newCupcakeResponse.data;
    const newCupcake = createCupcakeHTML(newCupcakeData.cupcake);
    document.getElementById("cupcakes-list").insertAdjacentHTML("beforeend", newCupcake);
    document.getElementById("new-cupcake-form").reset();
  });
  
  // Function to handle cupcake deletion
document.getElementById("cupcakes-list").addEventListener("click", async function (evt) {
    if (evt.target.classList.contains("delete-button")) {
        const cupcakeId = evt.target.closest("div").getAttribute("data-cupcake-id");
        await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
        evt.target.closest("div").remove();
    }
});
  
  // Show initial cupcakes when the page loads
showInitialCupcakes();