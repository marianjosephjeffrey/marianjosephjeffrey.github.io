document.addEventListener("DOMContentLoaded", function () {
    const username = "marianjosephjeffrey";  // Your GitHub username
    const apiUrl = `https://api.github.com/users/${username}/repos`;

    const projectContainer = document.getElementById("projects");

    fetch(apiUrl)
    .then(response => response.json())
    .then(repositories => {
        if (!Array.isArray(repositories)) {
            console.error("Invalid API response:", repositories);
            return;
        }

        // Filter out unwanted repos (like the default profile README repo)
        const filteredRepos = repositories.filter(repo => 
            repo.name !== username.toLowerCase() && !repo.fork
        );

        filteredRepos.forEach(repo => {
            const projectCard = document.createElement("div");
            projectCard.classList.add("project-card");

            projectCard.innerHTML = `
                <div class="project-details">
                    <h3>${repo.name.replace(/-/g, " ")}</h3>
                    <p>${repo.description ? repo.description : "No description available."}</p>
                    <div class="project-links">
                        <a href="${repo.html_url}" target="_blank">View on GitHub</a>
                    </div>
                </div>
            `;

            projectContainer.appendChild(projectCard);
        });
    })
    .catch(error => console.error("Error fetching GitHub projects:", error));
});