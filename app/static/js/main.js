// Initialize CodeMirror
const editor = CodeMirror.fromTextArea(document.getElementById('codeInput'), {
    lineNumbers: true,
    mode: 'python',
    theme: 'dracula',
    indentUnit: 4,
    lineWrapping: true
});

// Update CodeMirror mode when language changes
document.getElementById('languageSelect').addEventListener('change', function () {
    const language = this.value;
    let mode;

    switch (language) {
        case 'python': mode = 'python'; break;
        case 'javascript': mode = 'javascript'; break;
        case 'java':
        case 'cpp': mode = 'clike'; break;
        default: mode = 'python';
    }

    editor.setOption('mode', mode);
});

// Handle form submission
document.getElementById('codeForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    await generateImage();
});

// Handle preview button
document.getElementById('previewBtn').addEventListener('click', async function () {
    await generateImage(true);
});

// Generate image function
async function generateImage(previewOnly = false) {
    const formData = new FormData();
    formData.append('code', editor.getValue());
    formData.append('language', document.getElementById('languageSelect').value);
    formData.append('theme', document.getElementById('themeSelect').value);
    formData.append('font_size', document.getElementById('fontSize').value);
    formData.append('line_numbers', document.getElementById('lineNumbers').checked);
    formData.append('watermark', document.getElementById('addWatermark').checked);

    const fileInput = document.getElementById('fileUpload');
    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    }

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            body: formData
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            throw new Error(await response.text());
        }

        // Create object URL from response
        const blob = await response.blob();
        console.log("Received blob:", {
            size: blob.size,
            type: blob.type
        });

        const arrayBuffer = await blob.arrayBuffer();
        const header = new Uint8Array(arrayBuffer).slice(0, 8);

        const objectUrl = URL.createObjectURL(blob);

        // Display preview
        const previewImg = document.getElementById('previewImage');
        previewImg.onerror = function () {
            console.error("Image failed to load!");
            URL.revokeObjectURL(objectUrl);
        };

        previewImg.onload = function () {
            console.log("Image loaded successfully");
            URL.revokeObjectURL(objectUrl);
        };

        previewImg.src = objectUrl;
        previewImg.style.display = 'block';
        document.getElementById('previewPlaceholder').style.display = 'none';

        // Enable download button
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.disabled = false;
        downloadBtn.onclick = function () {
            const a = document.createElement('a');
            a.href = objectUrl;
            a.download = `code_snippet_${new Date().toISOString()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };

        if (!previewOnly) {
            // Show success message
            alert('Image generated successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating image: ' + error.message);
    }
}
// Real-time preview with debounce
let previewTimeout;
editor.on('change', function () {
    clearTimeout(previewTimeout);
    previewTimeout = setTimeout(updatePreview, 1000);
});

async function updatePreview() {
    const code = editor.getValue();
    if (!code.trim()) {
        document.getElementById('previewPlaceholder').style.display = 'block';
        document.getElementById('previewImage').style.display = 'none';
        return;
    }

    try {
        const response = await fetch('/api/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: document.getElementById('languageSelect').value,
                theme: document.getElementById('themeSelect').value,
                font_size: parseInt(document.getElementById('fontSize').value),
                line_numbers: document.getElementById('lineNumbers').checked
            })
        });

        if (!response.ok) throw new Error('Preview failed');

        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        const previewImg = document.getElementById('previewImage');

        // Clean up previous object URL if exists
        if (previewImg.src.startsWith('blob:')) {
            URL.revokeObjectURL(previewImg.src);
        }

        previewImg.onload = function () {
            URL.revokeObjectURL(objectUrl); // Clean up memory
        };
        previewImg.src = objectUrl;
        previewImg.style.display = 'block';
        document.getElementById('previewPlaceholder').style.display = 'none';
    } catch (error) {
        console.error('Preview error:', error);
    }
}