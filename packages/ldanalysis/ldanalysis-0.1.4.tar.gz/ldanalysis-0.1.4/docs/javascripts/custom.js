// Custom JavaScript for LDA Documentation

// Initialize terminal animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate terminal text typing effect
    const terminals = document.querySelectorAll('.terminal-demo');
    
    terminals.forEach(terminal => {
        const lines = terminal.querySelectorAll('.terminal-content > div');
        let delay = 0;
        
        lines.forEach((line, index) => {
            line.style.opacity = '0';
            line.style.animation = `fadeIn 0.5s ease-out ${delay}s forwards`;
            delay += 0.8;
        });
    });
    
    // Add copy functionality to code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.5rem;
            font-size: 0.875rem;
            background: #2E7D32;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(button);
        
        block.parentElement.addEventListener('mouseenter', () => {
            button.style.opacity = '1';
        });
        
        block.parentElement.addEventListener('mouseleave', () => {
            button.style.opacity = '0';
        });
        
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent);
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add interactive hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Terminal typing animation
    function typeTerminalText(element, text, speed = 50) {
        let index = 0;
        element.textContent = '';
        
        function type() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    // Initialize typing animation for demo terminal
    const demoCommands = document.querySelectorAll('.terminal-command');
    demoCommands.forEach((cmd, index) => {
        setTimeout(() => {
            typeTerminalText(cmd, cmd.textContent);
        }, index * 2000);
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Cmd/Ctrl + K for search
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.md-search__input');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close search
        if (e.key === 'Escape') {
            const searchInput = document.querySelector('.md-search__input');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
            }
        }
    });
    
    // Add loading animation for slow connections
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.animation = 'fadeIn 0.3s ease-out';
        });
    });
    
    // Highlight current section in navigation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                const navLink = document.querySelector(`nav a[href="#${id}"]`);
                if (navLink) {
                    document.querySelectorAll('nav a').forEach(link => {
                        link.classList.remove('active');
                    });
                    navLink.classList.add('active');
                }
            }
        });
    }, {
        rootMargin: '-20% 0px -70% 0px'
    });
    
    document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
        observer.observe(heading);
    });
    
    // Add progress indicator for long pages
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: #2E7D32;
        z-index: 1000;
        transition: width 0.2s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / scrollHeight) * 100;
        progressBar.style.width = progress + '%';
    });
    
    // Add mermaid diagram support
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ 
            theme: 'default',
            themeVariables: {
                primaryColor: '#2E7D32',
                primaryTextColor: '#fff',
                primaryBorderColor: '#1B5E20',
                lineColor: '#5c7cfa',
                secondaryColor: '#FFC107',
                background: '#f5f5f5',
                mainBkg: '#2E7D32',
                secondBkg: '#FFC107',
                tertiaryColor: '#fff'
            }
        });
    }
});

// Feedback widget
function initFeedbackWidget() {
    const feedbackButton = document.createElement('button');
    feedbackButton.innerHTML = '💬 Feedback';
    feedbackButton.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        padding: 0.75rem 1.5rem;
        background: #2E7D32;
        color: white;
        border: none;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 100;
        transition: all 0.3s ease;
    `;
    
    feedbackButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
        this.style.boxShadow = '0 6px 12px rgba(0,0,0,0.3)';
    });
    
    feedbackButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
    });
    
    feedbackButton.addEventListener('click', function() {
        window.open('https://github.com/drpedapati/LDA/issues/new', '_blank');
    });
    
    document.body.appendChild(feedbackButton);
}

// Initialize feedback widget when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFeedbackWidget);
} else {
    initFeedbackWidget();
}