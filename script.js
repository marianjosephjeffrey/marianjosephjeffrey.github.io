document.addEventListener("DOMContentLoaded", function () {
    console.log("Script Loaded: Fetching data...");

    fetchMediumPosts();         // Load Medium Blog Posts
    fetchGitHubContributions(); // Load GitHub Contributions
    fetchProjectsFromLinkedIn(); // Load LinkedIn Projects

    fetchComponent("header.html", "header-container"); // Load Header
    fetchComponent("footer.html", "footer-container"); // Load Footer

    const darkModeToggle = document.getElementById("dark-mode-toggle");
    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
        });
    }
});

// ✅ Function: Fetch Medium Posts (With Description)
function fetchMediumPosts() {
    const mediumUsername = "mjcube1999"; // Your Medium username
    const rssFeedUrl = `https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@${mediumUsername}`;

    fetch(rssFeedUrl)
        .then(response => response.json())
        .then(data => {
            console.log("Medium API Response:", data);

            const postsContainer = document.getElementById("medium-posts");
            if (!postsContainer) return;

            postsContainer.innerHTML = ""; // Clear previous content

            if (data.status === "ok" && data.items.length > 0) {
                data.items.slice(0, 20).forEach(item => { // Limit to 6 latest posts
                    const card = document.createElement("div");
                    card.className = "card";

                    // ✅ Extract Thumbnail Image
                    let imgSrc = "default-image.jpg"; // Fallback image
                    const imgRegex = /<img.*?src=["'](.*?)["']/; // Regex to extract img URL
                    const match = imgRegex.exec(item.content);
                    if (match) {
                        imgSrc = match[1]; // Use extracted image
                    }

                    // ✅ Extract Text Content (Stripped HTML)
                    const tempDiv = document.createElement("div");
                    tempDiv.innerHTML = item.content; // Convert HTML to DOM element
                    let description = tempDiv.textContent || tempDiv.innerText || "";
                    description = description.replace(/\s+/g, " ").trim(); // Clean up spaces
                    description = description.substring(0, 150) + "..."; // Limit to 150 chars

                    card.innerHTML = `
                        <img src="${imgSrc}" alt="Medium Post Image">
                        <h2>${item.title}</h2>
                        <p class="post-description">${description}</p>
                        <p class="post-date">${new Date(item.pubDate).toDateString()}</p>
                        <a href="${item.link}" target="_blank">Read More</a>
                    `;
                    postsContainer.appendChild(card);
                });
            } else {
                postsContainer.innerHTML = "<p>No recent Medium posts found.</p>";
            }
        })
        .catch(error => console.error("Error fetching Medium posts:", error));
}


// ✅ Function: Fetch Header & Footer
function fetchComponent(url, containerId) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const container = document.getElementById(containerId);
            if (container) container.innerHTML = data;
        })
        .catch(error => console.error(`Error loading ${url}:`, error));
}