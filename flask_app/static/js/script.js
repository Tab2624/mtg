// Function to open the custom modal
function openCustomModal(imageSrc) {
  const modal = document.getElementById("customImageModal");
  const modalImage = document.getElementById("customModalImage");
  modalImage.src = imageSrc;
  modal.style.display = "block";
}

// Function to close the custom modal
function closeCustomModal() {
  const modal = document.getElementById("customImageModal");
  modal.style.display = "none";
}

// Get all the images with the class 'custom-modal-image' and add click event listeners
const images = document.getElementsByClassName("custom-modal-image");
const imagesArray = Array.from(images); // Convert HTMLCollection to an array
imagesArray.forEach((image) => {
  image.addEventListener("click", () => {
    openCustomModal(image.src);
  });
});

// Close the custom modal when clicking the close button
const closeModalButton = document.getElementById("customCloseModal");
closeModalButton.addEventListener("click", () => {
  closeCustomModal();
});

// Close the custom modal when clicking outside the image
window.addEventListener("click", (event) => {
  const modal = document.getElementById("customImageModal");
  if (event.target === modal) {
    closeCustomModal();
  }
});

// Get the custom modal and buttons
const customModal = document.getElementById("customModal");
const customNewDeckButton = document.getElementById("customNewDeckButton");
const customCloseModalButton = document.getElementById("customCloseModal");
const customSaveDeckButton = document.getElementById("customSaveDeckButton");
const customDeckNameInput = document.getElementById("customDeckNameInput");

// Initially, hide the custom modal
customModal.style.display = "none";

// When the Custom New Deck button is clicked, show the custom modal
customNewDeckButton.addEventListener("click", function () {
  customModal.style.display = "block";
});

// When the Custom Close button is clicked, hide the custom modal
customCloseModalButton.addEventListener("click", function () {
  customModal.style.display = "none";
  customDeckNameInput.value = ""; // Clear the input field
});

// When the Custom Save button is clicked, handle the custom deck name input
customSaveDeckButton.addEventListener("click", function () {
  const customDeckName = customDeckNameInput.value;
  // Do something with the custom deck name, e.g., save it to your application.
  console.log("Custom Deck Name:", customDeckName);
  customModal.style.display = "none";
  customDeckNameInput.value = ""; // Clear the input field
});


