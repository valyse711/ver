// AES key must match your C++ key (32 bytes)
const AES_KEY = new Uint8Array([
    0x9f, 0xa1, 0x3c, 0x8d, 0x7e, 0x5b, 0x12, 0x4a,
    0xbb, 0xef, 0x90, 0x67, 0xd4, 0x21, 0xfa, 0x3c,
    0x88, 0x11, 0x66, 0x2a, 0x99, 0xcd, 0x57, 0x0b,
    0x3e, 0x44, 0xde, 0x71, 0x8f, 0x0a, 0x23, 0x5c
]);

const output = document.getElementById('output');

document.getElementById('check-version').addEventListener('click', async () => {
    output.textContent = 'Checking...';

    try {
        // Replace this URL with your JSON file on GitHub Pages
        const response = await fetch('version.json');
        const data = await response.json();

        const iv = Uint8Array.from(atob(data.iv), c => c.charCodeAt(0));
        const ciphertext = Uint8Array.from(atob(data.data), c => c.charCodeAt(0));

        const key = await crypto.subtle.importKey(
            'raw',
            AES_KEY,
            { name: 'AES-CBC' },
            false,
            ['decrypt']
        );

        const decryptedBuffer = await crypto.subtle.decrypt(
            { name: 'AES-CBC', iv },
            key,
            ciphertext
        );

        const decoder = new TextDecoder();
        const plaintext = decoder.decode(decryptedBuffer);
        output.textContent = "Decrypted JSON:\n" + plaintext;
    } catch (err) {
        output.textContent = 'Error: ' + err;
    }
});
