# Building a Blog with Cloudflare, Wrangler, and GitHub

In this tutorial, we will walk through the steps of adding a blog to your website hosted on Cloudflare Workers. I host my personal website's homepage using this service, but the methods outlined here can be applied to other hosting platforms as well.

The blog will use an HTML template, and the content will be written and committed in Markdown format. Upon committing to your GitHub repository, your new blogpost will be automatically deployed to Cloudflare using Wrangler.

## **Prerequisites**

1. A GitHub account
2. A command line interface (like Terminal on Mac, CMD on Windows)
3. Installed copies of git, Python, and Wrangler on your computer
4. A Cloudflare account

## **Step 1: Setting up the GitHub Repository**

Start by creating a new repository on GitHub. You could also use an existing repository if you'd like. For the purpose of this tutorial, let's assume the name of the repository is "my-website". Clone this repository to your local machine using the following command in your terminal:

```
git clone https://github.com/yourusername/my-website.git
```

Navigate into the "my-website" directory using `cd my-website`.

Inside "my-website" directory, create the directory path "webroot/blog/content". In "webroot", we will store our HTML index file and in "webroot/blog/content" our individual blog posts. Use the following commands to create these directories: `mkdir -p webroot/blog/content`

## **Step 2: Creating the HTML Index**

Inside the "webroot" directory, create a new HTML file. This will be the HTML template for your blog. Let’s name it `index.html``.

In "index.html":

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Blog</title>
  </head>
  <body>
    <div id="content">
      <!-- The Markdown blog post will be loaded here -->
    </div>

    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/showdown/2.1.0/showdown.min.js"
      integrity="sha512-LhccdVNGe2QMEfI3x4DVV3ckMRe36TfydKss6mJpdHjNFiV07dFpS2xzeZedptKZrwxfICJpez09iNioiSZ3hA=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    ></script>
    <script>
      // Get the current URL
      let url = window.location.pathname;
      // Ensure trailing slash is removed, if present
      if (url.endsWith("/")) {
        url = url.slice(0, -1);
      }

      // Add /content to the URL just after the blog directory
      url = url.replace("/blog/", "/blog/content/");

      // Append '.md' to the URL
      const mdFileUrl = `${url}.md`;

      fetch(mdFileUrl)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Not 2xx response");
          }
          return response.text();
        })
        .then((text) => {
          var converter = new showdown.Converter();
          var html = converter.makeHtml(text);
          document.getElementById("content").innerHTML = html;
        })
        .catch((error) => {
          // Handle the error
          if (error.message === "Not 2xx response") {
            document.title = "404 Article Not Found";
            document.getElementById("content").innerHTML =
              "<h1>404</h1><p>Article Not Found</p>";
          } else {
            // Handle other errors (like network errors)
            document.title = "Error Loading Article";
            document.getElementById("content").innerHTML =
              "<h1>Error</h1><p>There was an issue loading the article. Please try again later.</p>";
          }
        });
    </script>
  </body>
</html>
```

This is a basic example, but you can customize it as you wish.

## **Step 3: Writing your First Blog Post**

Create a new .md file inside the "webroot/blog/content" directory. Let's call it "first-post.md".

Write something like this:

```
# My First Blog Post

Hello, world! This is my first blog post.
```

## **Step 4: Wiring up Cloudflare Workers**

At this point, our code is ready to deploy with the help of [Cloudflare Workers](https://developers.cloudflare.com/workers/), which allow us to serve content directly from the edge of Cloudflare's network. To set this up:

1. Sign into your Cloudflare account.
2. From the Accounts Home, choose your domain.
3. On the next page, scroll down and click on the "Workers" icon under "Advanced Actions".
4. Click "Create a Worker".
5. Name the Worker "blog", then click "Create and Deploy".
6. In the Worker script, replace the existing code with the following:

```javascript
addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  // Fetch the original request
  const response = await fetch(request);

  // If the request is for a blog page
  if (request.url.endsWith(".md")) {
    // Fetch the markdown content
    const md = await fetch(
      `https://github.com/yourusername/my-website/raw/main/webroot/${
        new URL(request.url).pathname
      }`
    );

    // Convert to HTML using the showdown library
    const html = new showdown.Converter().makeHtml(await md.text());

    // Create a new response with the same status and headers as the original response
    const newResponse = new Response(response.body, response);
    // Set the Content-Type header to 'text/html'
    newResponse.headers.set("Content-Type", "text/html");
    // Set the body of the response to the converted HTML
    newResponse.body = `<html><body>${html}</body></html>`;

    // Return the new response
    return newResponse;
  }

  // Otherwise, return the original response
  return response;
}
```

7. Click "Save and Deploy" to deploy the new Worker.

## **Step 5: Configuring Wrangler**

Before we can use Wrangler to deploy our site to Cloudflare, we need to configure it. Run `wrangler config` and follow the prompts. Copy `account_id` from the Workers section of the Cloudflare dashboard and paste it into Wrangler.

To configure GitHub Actions to deploy our blog posts to Cloudflare, create a `.github/workflows/deploy.yml` file in your GitHub repository and input the following:

```yml
name: Worker Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Generate
        run: wrangler generate my-blog

      - name: Publish
        run: wrangler publish --env production
        env:
          CF_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
```

This configures your GitHub repository to redeploy every time changes are pushed to the main branch. Be sure to set the `CF_API_TOKEN` secret to your Cloudflare API token.

Remember to do `git add .`, `git commit -m "Added: Wrangler configuration and GitHub Actions"` and `git push origin main` to your repository. You can check the "Actions" tab in GitHub to see that your new blog post is being deployed to Cloudflare.

Your blog is now completely set up!
