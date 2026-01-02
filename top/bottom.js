// let selectedTops = [];
// let selectedBottoms = [];
// let selectedOccasion = null;
// let stylingList = [];
// let stylingData = {};

// // Select all wardrobe buttons for tops and bottoms
// const topButtons = document.querySelectorAll('.wardrobe-button.t'); // Add .t class to top buttons
// const bottomButtons = document.querySelectorAll('.wardrobe-button.b'); // Bottom buttons

// // Function to handle button click and toggle selection for tops
// function handleTopClick(event) {
//     const button = event.target;
//     const buttonText = button.textContent;

//     if (button.classList.contains('selected')) {
//         selectedTops = selectedTops.filter(item => item !== buttonText);
//         button.classList.remove('selected');
//     } else {
//         selectedTops.push(buttonText);
//         button.classList.add('selected');
//     }

//     // Store the selected tops in localStorage
//     localStorage.setItem('selectedTops', JSON.stringify(selectedTops));
//     console.log('Selected Tops:', selectedTops);
// }

// // Add event listener to each top button
// topButtons.forEach(button => {
//     button.addEventListener('click', handleTopClick);
// });

// // Function to navigate to the next page for tops
// function nextTops(event) {
//     event.preventDefault(); // Prevent default action
//     window.location.href = 'bottom.html'; // Navigate to bottoms page
// }
// document.querySelector('.next-button.bot').addEventListener('click', nextTops);

// // Function to handle button click and toggle selection for bottoms
// function handleBottomClick(event) {
//     const button = event.target;
//     const buttonText = button.textContent;

//     if (button.classList.contains('selected')) {
//         selectedBottoms = selectedBottoms.filter(item => item !== buttonText);
//         button.classList.remove('selected');
//     } else {
//         selectedBottoms.push(buttonText);
//         button.classList.add('selected');
//     }

//     // Store the selected bottoms in localStorage
//     localStorage.setItem('selectedBottoms', JSON.stringify(selectedBottoms));
//     console.log('Selected Bottoms:', selectedBottoms);
// }

// // Add event listener to each bottom button
// bottomButtons.forEach(button => {
//     button.addEventListener('click', handleBottomClick);
// });

// // Function to navigate to the next page for bottoms
// function nextBottoms(event) {
//     event.preventDefault(); 
//     window.location.href = 'occasion.html'; 
// }
// document.querySelector('.next-button.bot').addEventListener('click', nextBottoms);

// // Select occasion buttons
// const occasionButtons = document.querySelectorAll('.wardrobe-button.o'); // Ensure occasion buttons have the class .o

// // Function to handle occasion selection
// function handleOccasionClick(event) {
//     occasionButtons.forEach(button => button.classList.remove('selected')); // Remove selected class from all buttons

//     const button = event.target;
//     button.classList.add('selected');
//     selectedOccasion = button.textContent;

//     // Store the selected occasion in localStorage
//     localStorage.setItem('selectedOccasion', selectedOccasion);
//     console.log('Selected Occasion:', selectedOccasion);
// }

// // Add event listener to each occasion button
// occasionButtons.forEach(button => {
//     button.addEventListener('click', handleOccasionClick);
// });

// // Fetch styling combinations from JSON file
// fetch('outfits.json')
//     .then(response => response.json())
//     .then(data => {
//         stylingData = data;
//         console.log('Styling Data Loaded:', stylingData);
//     })
//     .catch(error => console.error('Error loading JSON:', error));

// // Function to filter styling combinations based on selections
// function filterStylingCombinations() {
//     let occasionData = stylingData[selectedOccasion];
//     selectedTops.forEach(top => {
//         selectedBottoms.forEach(bottom => {
//             occasionData.forEach(combo => {
//                 if (combo.Top === top && combo.Bottom === bottom) {
//                     stylingList.push({ top, bottom });
//                 }
//             });
//         });
//     });
//     console.log("Styling List: ", stylingList);
// }

// // Function to handle navigation to the results page
// function handleNext() {
//     filterStylingCombinations();
//     window.location.href = 'result.html'; 
// }

// // Assuming you have a button for results page navigation
// document.querySelector('.next-button.results').addEventListener('click', handleNext);
