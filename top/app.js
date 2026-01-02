// let selectedTops = [];

// let selectedBottoms = [];

// const topButtons = document.querySelectorAll('.wardrobe-button.t');
// const bottomButtons = document.querySelectorAll('.wardrobe-button.b');
// console.log(bottomButtons)
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

// topButtons.forEach(button => {
//     button.addEventListener('click', handleTopClick);
// });
// function nextTops(event) {
//     event.preventDefault(); // Prevent default action
//     window.location.href = 'bottom.html'; // Navigate to bottoms page
// }
// document.querySelector('.next-button.top').addEventListener('click', nextTops);

// // Function to handle button click and toggle selection for bottoms
// function handleBottomClick(event) {
//     console.log("bottom")
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

//  // Assuming you have a container
// bottomButtons.forEach(button => { 
//     button.addEventListener('click', handleBottomClick);
//     console.log("bot")
// });

// function nextBottoms(event) {
//     event.preventDefault(); 
//     window.location.href = 'occasion.html'; 
// }
// document.querySelector('.next-button.bot').addEventListener('click', nextBottoms);

// let selectedOccasion = null;

// const occasionButtons = document.querySelectorAll('.wardrobe-button.o');

// function handleOccasionClick(event) {

//     const button = event.target;
//     button.classList.add('selected');
//     selectedOccasion = button.textContent;
    
//     localStorage.setItem('selectedOccasion', selectedOccasion);

//     console.log('Selected Occasion:', selectedOccasion);
// }


// // Add event listener to each occasion button
// occasionButtons.forEach(button => {
//     button.addEventListener('click', handleOccasionClick);
// });



// let stylingList = [];
// let stylingData = {}
// fetch('outfits.json')
//     .then(response => response.json())
//     .then(data => {
//         stylingData = data;
//         console.log('Styling Data Loaded:', stylingData);
//     })
//     .catch(error => console.error('Error loading JSON:', error));
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
// function handleNext() {
//     filterStylingCombinations();
//     window.location.href = 'result.html';
// }

// document.querySelector('.next-button.results').addEventListener('click', handleNext);
