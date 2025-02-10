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