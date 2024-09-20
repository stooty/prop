document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const proposalOutput = document.getElementById('proposalOutput');
    const proposalContent = document.getElementById('proposalContent');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const resumeFile = document.getElementById('resume').files[0];
        const jobDescriptionFile = document.getElementById('jobDescription').files[0];
        
        if (!resumeFile || !jobDescriptionFile) {
            alert('Please upload both resume and job description files.');
            return;
        }
        
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('jobDescription', jobDescriptionFile);
        
        try {
            const response = await fetch('upload.php', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('File upload failed');
            }
            
            const result = await response.json();
            
            if (result.success) {
                const proposal = await generateProposal(result.resumeId, result.jobDescriptionId);
                displayProposal(proposal);
            } else {
                throw new Error(result.message || 'An error occurred');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
    
    async function generateProposal(resumeId, jobDescriptionId) {
        // API-Needed: Replace this with actual API call to Claude
        const response = await fetch('ClaudeAPI', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resumeId, jobDescriptionId })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate proposal');
        }
        
        return await response.json();
    }
    
    function displayProposal(proposal) {
        proposalContent.innerHTML = proposal.content;
        proposalOutput.classList.remove('hidden');
    }
});
