---
title: Home
description: Linked Document Analysis - Track every change. Map every connection.
hide:
  - navigation
  - toc
---

<style>
.md-main__inner {
  margin: 0;
}
.md-content {
  max-width: none;
  margin: 0;
  padding: 0;
}
.hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(58,83,164,0.05) 0%, transparent 70%);
  animation: pulse 30s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
.hero-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  position: relative;
  z-index: 1;
}
.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #3a53a4;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.hero-tagline {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 1.5rem;
  font-weight: 300;
}
.hero-description {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 3rem;
  line-height: 1.6;
}
.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}
.hero-button {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 1.1rem;
}
.hero-button-primary {
  background: #3a53a4;
  color: white;
  box-shadow: 0 4px 6px rgba(58,83,164,0.2);
}
.hero-button-primary:hover {
  background: #2c3e7d;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(58,83,164,0.3);
}
.hero-button-secondary {
  background: white;
  color: #3a53a4;
  border: 2px solid #3a53a4;
}
.hero-button-secondary:hover {
  background: #e8ebf5;
  transform: translateY(-2px);
}
.terminal-demo {
  margin-top: 4rem;
  background: #1E1E1E;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
.terminal-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.terminal-dots {
  display: flex;
  gap: 0.5rem;
}
.terminal-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.terminal-dot-red {
  background: #FF5F56;
}
.terminal-dot-yellow {
  background: #FFBD2E;
}
.terminal-dot-green {
  background: #27C93F;
}
.terminal-content {
  font-family: 'JetBrains Mono', monospace;
  color: #00FF00;
  font-size: 0.9rem;
  line-height: 1.6;
}
.terminal-prompt {
  color: #00FF00;
}
.terminal-command {
  color: #FFFFFF;
}
.terminal-output {
  color: #B0B0B0;
  margin-left: 1rem;
}
.section {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 3rem;
  color: #3a53a4;
}
.quick-start {
  background: #F5F5F5;
}
.installation-steps {
  max-width: 600px;
  margin: 0 auto;
}
.step {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}
.step:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}
.step-number {
  display: inline-block;
  width: 32px;
  height: 32px;
  background: #3a53a4;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 32px;
  font-weight: 700;
  margin-right: 1rem;
}
.step-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}
.step-content {
  color: #666;
  line-height: 1.6;
}
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}
.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  text-align: center;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}
.feature-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #3a53a4;
}
.feature-description {
  color: #666;
  line-height: 1.6;
}
.cta-section {
  background: #3a53a4;
  color: white;
  text-align: center;
  padding: 4rem 2rem;
}
.cta-title {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.cta-description {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}
</style>

<div class="hero">
  <div class="hero-content">
    <img src="assets/Logo.svg" alt="LDA Logo" style="max-width: 400px; margin: 0 auto 2rem; display: block;">
    <h1>Linked Document Analysis</h1>
    <p class="hero-tagline">Track every change. Map every connection.</p>
    <p class="hero-description">
      The intelligent project management tool that creates a living map of your documents, 
      tracking relationships, monitoring changes, and preserving your project's complete history.
    </p>
    <div class="hero-actions">
      <a href="#quick-start" class="hero-button hero-button-primary">Get Started</a>
      <a href="#demo" class="hero-button hero-button-secondary">View Demo</a>
    </div>
    <div class="terminal-demo" id="demo">
      <div class="terminal-header">
        <div class="terminal-dots">
          <div class="terminal-dot terminal-dot-red"></div>
          <div class="terminal-dot terminal-dot-yellow"></div>
          <div class="terminal-dot terminal-dot-green"></div>
        </div>
      </div>
      <div class="terminal-content">
        <div>
          <span class="terminal-prompt">$</span>
          <span class="terminal-command"> lda init</span>
        </div>
        <div class="terminal-output">✨ Initializing new project...</div>
        <div class="terminal-output">📁 Created project structure</div>
        <div class="terminal-output">✅ Project ready!</div>
        <br>
        <div>
          <span class="terminal-prompt">$</span>
          <span class="terminal-command"> lda track</span>
        </div>
        <div class="terminal-output">🔍 Tracking files...</div>
        <div class="terminal-output">📊 Found 12 files</div>
        <div class="terminal-output">✅ All files tracked</div>
        <br>
        <div>
          <span class="terminal-prompt">$</span>
          <span class="terminal-command"> lda status</span>
        </div>
        <div class="terminal-output">📈 Project: Research Analysis</div>
        <div class="terminal-output">📝 3 documents modified</div>
        <div class="terminal-output">🔗 7 linked references</div>
      </div>
    </div>
  </div>
</div>

<section class="section quick-start" id="quick-start">
  <h2 class="section-title">Quick Start</h2>
  <div class="installation-steps">
    <div class="step">
      <div class="step-title">
        <span class="step-number">1</span>Install LDA
      </div>
      <div class="step-content">
        <pre><code class="language-bash">pip install lda-analysis</code></pre>
        <p>Works with Python 3.8+ on Windows, macOS, and Linux.</p>
      </div>
    </div>
    
    <div class="step">
      <div class="step-title">
        <span class="step-number">2</span>Initialize Your Project
      </div>
      <div class="step-content">
        <pre><code class="language-bash">lda init</code></pre>
        <p>Creates project structure and configuration file.</p>
      </div>
    </div>
    
    <div class="step">
      <div class="step-title">
        <span class="step-number">3</span>Track Your Files
      </div>
      <div class="step-content">
        <pre><code class="language-bash">lda track</code></pre>
        <p>Monitors all project files for changes and connections.</p>
      </div>
    </div>
    
    <div class="step">
      <div class="step-title">
        <span class="step-number">4</span>View Status
      </div>
      <div class="step-content">
        <pre><code class="language-bash">lda status</code></pre>
        <p>See your project's current state and recent changes.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Features</h2>
  <div class="feature-grid">
    <div class="feature-card">
      <div class="feature-icon">🔗</div>
      <div class="feature-title">Document Linking</div>
      <div class="feature-description">
        Automatically map relationships between documents, tracking citations, 
        references, and dependencies.
      </div>
    </div>
    
    <div class="feature-card">
      <div class="feature-icon">📊</div>
      <div class="feature-title">Change Tracking</div>
      <div class="feature-description">
        Monitor all file modifications with detailed history, diffs, and 
        rollback capabilities.
      </div>
    </div>
    
    <div class="feature-card">
      <div class="feature-icon">🏗️</div>
      <div class="feature-title">Project Scaffolding</div>
      <div class="feature-description">
        Generate consistent project structures from templates, ensuring 
        standardized organization.
      </div>
    </div>
    
    <div class="feature-card">
      <div class="feature-icon">📝</div>
      <div class="feature-title">Smart Templates</div>
      <div class="feature-description">
        Pre-configured templates for research, documentation, and development 
        projects.
      </div>
    </div>
    
    <div class="feature-card">
      <div class="feature-icon">🔍</div>
      <div class="feature-title">File Monitoring</div>
      <div class="feature-description">
        Real-time detection of file changes, additions, and deletions with 
        integrity verification.
      </div>
    </div>
    
    <div class="feature-card">
      <div class="feature-icon">📦</div>
      <div class="feature-title">Export Reports</div>
      <div class="feature-description">
        Generate comprehensive reports in multiple formats including HTML, 
        PDF, and CSV.
      </div>
    </div>
  </div>
</section>

<section class="cta-section">
  <h2 class="cta-title">Ready to Transform Your Workflow?</h2>
  <p class="cta-description">
    Join thousands of researchers and developers using LDA to manage their projects.
  </p>
  <div class="hero-actions">
    <a href="getting-started/installation/" class="hero-button hero-button-primary">
      Get Started Now
    </a>
    <a href="user-guide/concepts/" class="hero-button hero-button-secondary" style="background: white; color: #3a53a4;">
      Read the Docs
    </a>
  </div>
</section>