document.addEventListener('DOMContentLoaded', () => {
    const nextBtn = document.getElementById('next-btn');
    const questionTextElement = document.getElementById('question-text');
    const optionsContainer = document.getElementById('options-container');

    // Function to load the question and its options
    function loadQuestion(question) {
        // Set the question text
        questionTextElement.innerText = question[1]; // Assuming question text is in the second column

        // Clear previous options
        optionsContainer.innerHTML = '';

        // Create and add options dynamically
        const optionValues = [question[2], question[3], question[4], question[5]];
        optionValues.forEach(value => {
            const optionWrapper = document.createElement('div');
            optionWrapper.classList.add('option');

            const label = document.createElement('label');
            label.innerHTML = `<input type="radio" name="option" value="${value}" required> ${value}`;
            optionWrapper.appendChild(label);

            optionsContainer.appendChild(optionWrapper);
        });
    }

    // Event listener for the Next Question button
    nextBtn.addEventListener('click', (event) => {
        event.preventDefault();
        const selectedOption = document.querySelector('input[name="option"]:checked');

        if (selectedOption) {
            fetchNextQuestion(selectedOption.value);
        } else {
            alert('Please select an option!');
        }
    });

    // Function to fetch the next question
    function fetchNextQuestion(selectedOption) {
        fetch('/next_question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selected_option: selectedOption })
        })
        .then(response => response.json())
        .then(data => {
            if (data.finished) {
                window.location.href = '/submit_quiz';
            } else {
                loadQuestion(data.question);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Load the first question on page load
    loadQuestion({{ question | tojson }});
});
