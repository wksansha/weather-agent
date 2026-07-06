 // 引入 marked.js CDN（放在 head 中）
// <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

const showDocsBtn = document.getElementById('showDocsBtn');
const docsContainer = document.getElementById('docsContainer');
const messagesContainer = document.getElementById('messages');
let docsVisible = false;

showDocsBtn.addEventListener('click', async () => {
    docsVisible = !docsVisible;
    if (docsVisible) {
        // 切换显示文档区域，隐藏聊天
        messagesContainer.style.display = 'none';
        docsContainer.style.display = 'block';
        // 如果文档未加载，则请求
        if (!docsContainer.dataset.loaded) {
            try {
                const response = await fetch('/docs/README.md'); // 或你的 md 文件路径
                if (!response.ok) throw new Error('文档加载失败');
                const mdContent = await response.text();
                // 使用 marked 渲染
                docsContainer.innerHTML = marked.parse(mdContent);
                docsContainer.dataset.loaded = 'true';
            } catch (error) {
                docsContainer.innerHTML = `<p style="color:red;">❌ 文档加载失败: ${error.message}</p>`;
            }
        }
    } else {
        // 切回聊天
        messagesContainer.style.display = 'flex';
        docsContainer.style.display = 'none';
    }
});