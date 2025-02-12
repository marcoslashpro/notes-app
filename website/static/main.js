// searches for notes in the navbar
document.addEventListener('DOMContentLoaded', function () {
	let searchInput = document.getElementById('searchInput');
	let searchDisplay = document.getElementById('searchDisplay');

	searchInput.addEventListener('input', function () {
		let query = searchInput.value;
		
		if (query.length > 0) {
			fetch('/search-note', {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ query: query })
			})
			.then(_res => _res.json())
			.then(data => {
				for (let note of data) {

					searchDisplay.innerHTML = "";
					let itemHTML = document.createElement("a");
					itemHTML.textContent = note.title;
					itemHTML.className = "dropdown-item";
					itemHTML.href = `/get-note/${note.id}`

					searchDisplay.appendChild(itemHTML)
					searchDisplay.style.display = "block";
				}
			})

		} else {
			searchDisplay.style.display = "none"
		};
	})
	document.addEventListener('click', function(event) {
		if (!searchDisplay.contains(event.target) && event.target !== searchInput) {
			searchDisplay.style.display = "none";
			searchInput.value = "";
		}
	});
});


function displayMessage(message, templateId, contentClass, containerId) {
    const template = document.getElementById(templateId);
    const container = document.getElementById(containerId);

    if (message.length > 0) {
        let cloneTemplate = template.content.cloneNode(true);
        let content = cloneTemplate.querySelector(contentClass);

        if (content) { 
            content.textContent = message;
            content.style.display = 'block';
            
            container.appendChild(cloneTemplate);
        } else {
            console.error(`Element with class '${contentClass}' not found in template.`);
        }
    }
}



async function sendMessage() {
	let query = document.getElementById('chatInput');

	// Display user's message
	displayMessage(
		message=query.value,
		templateId='userMessageTemplate',
		contentClass='.human-message',
		containerId='messageBox'
	);

	query.value = '' //keeps input field clean

	const textDecoder = new TextDecoder();

	// Send request to server
	let response = await fetch('/Jarvis/talk-ai', {
		headers: {
			"Content-Type": "application/json"
		},
		method: "POST",
		body: JSON.stringify({ query: query.value })
	});

	if (!response.body) throw new Error("ReadableStream not supported");

	const reader = response.body.getReader();

	let template = document.getElementById('aiMessageTemplate');
	let container = document.getElementById('messageBox');

	if (!template || !container) {
	    console.error("Template or container element not found!");
	    return;
	}

	  // Create the clone *outside* the readStream function
	let cloneTemplate = template.content.cloneNode(true);
	let content = cloneTemplate.querySelector('.ai-message');

	if (!content) {
	    console.error("Element with class 'ai-message' not found in template.");
	    return;
	}


	async function readStream() {
	    try {
	      // Append the clone *after* the stream is ready but before the first chunk is read.
	      container.appendChild(cloneTemplate);

	      while (true) {
	        const { value, done } = await reader.read();
	        if (done) break;

	        const decoder = new TextDecoder();
	        const chunk = decoder.decode(value);

	        content.style.display = 'block'
	        content.textContent += chunk;
	        container.scrollTop = container.scrollHeight; // Keep scrolling
	      }
	    } catch (error) {
	      console.error("Error reading stream:", error);
	    }
	}

	readStream();
}




