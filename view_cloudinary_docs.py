"""
View Cloudinary Documents in Web Browser
"""

import cloudinary
import cloudinary.api
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

# Configure Cloudinary
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SW0",
    secure=True
)

class CloudinaryDocsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_main_page()
        elif self.path == '/documents':
            self.serve_documents_json()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Verified Documents in Cloudinary</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        .docs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .doc-card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 15px; }
        .doc-image { width: 100%; height: 200px; object-fit: cover; border-radius: 4px; }
        .doc-info { margin-top: 10px; }
        .doc-id { font-size: 12px; color: #666; word-break: break-all; }
        .loading { text-align: center; padding: 20px; }
        .error { color: red; text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>_verified Documents in Cloudinary</h1>
        <div id="docs-container" class="loading">Loading documents...</div>
    </div>

    <script>
        async function loadDocuments() {
            try {
                const response = await fetch('/documents');
                const data = await response.json();
                
                const container = document.getElementById('docs-container');
                
                if (data.error) {
                    container.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    return;
                }
                
                if (data.resources.length === 0) {
                    container.innerHTML = '<div>No verified documents found.</div>';
                    return;
                }
                
                const docsGrid = document.createElement('div');
                docsGrid.className = 'docs-grid';
                
                data.resources.forEach(doc => {
                    const docCard = document.createElement('div');
                    docCard.className = 'doc-card';
                    
                    docCard.innerHTML = `
                        <img src="${doc.secure_url}" alt="Verified Document" class="doc-image" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBGb3VuZDwvdGV4dD48L3N2Zz4=';">
                        <div class="doc-info">
                            <div class="doc-id">ID: ${doc.public_id}</div>
                            <div>Created: ${new Date(doc.created_at).toLocaleString()}</div>
                        </div>
                    `;
                    
                    docsGrid.appendChild(docCard);
                });
                
                container.innerHTML = '';
                container.appendChild(docsGrid);
                
            } catch (error) {
                document.getElementById('docs-container').innerHTML = 
                    `<div class="error">Failed to load documents: ${error.message}</div>`;
            }
        }
        
        // Load documents when page loads
        window.onload = loadDocuments;
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_documents_json(self):
        try:
            # List resources in the verified_documents folder
            resources = cloudinary.api.resources(
                type="upload",
                prefix="verified_documents/",
                max_results=100
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(resources).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

def run_server(port=8081):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CloudinaryDocsHandler)
    print(f"Starting server on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()