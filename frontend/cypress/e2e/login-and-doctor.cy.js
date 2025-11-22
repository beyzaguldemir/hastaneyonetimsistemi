describe('Login and Add Doctor Test', () => {
  const baseUrl = 'http://localhost:5173';
  const adminEmail = 'admin@hospital.com';
  const adminPassword = 'admin123';

  it('should login and add a new doctor', () => {
    // Step 1: Visit the application
    cy.visit(baseUrl);
    cy.wait(2000); // Sayfa yüklenmesi için bekle
    
    // Step 2: Verify we're on the login page
    cy.url().should('include', '/login');
    cy.wait(1000);
    cy.contains('Hastane Yönetim Sistemi').should('be.visible');
    cy.wait(1000);
    
    // Step 3: Fill in login form
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(1000);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(1000);
    
    // Step 4: Submit login form
    cy.get('button[type="submit"]').click();
    cy.wait(2000);
    
    // Step 5: Wait for redirect to dashboard
    cy.url().should('include', '/dashboard');
    cy.wait(2000);
    cy.contains('Dashboard').should('be.visible');
    cy.wait(2000);
    
    // Step 6: Navigate to Doctors page
    cy.contains('Doktorlar').click();
    cy.wait(2000);
    cy.url().should('include', '/doctors');
    cy.wait(2000);
    cy.contains('Doktorlar').should('be.visible');
    cy.wait(2000);
    
    // Step 7: Click on "Yeni Doktor" button
    cy.contains('+ Yeni Doktor').click();
    cy.wait(2000);
    
    // Step 8: Fill in doctor form
    const doctorName = `Dr. Test Doktor ${Date.now()}`;
    const doctorEmail = `drtest${Date.now()}@example.com`;
    const doctorPhone = '05321112233';
    const doctorSpecialization = 'Kardiyolog';
    
    // Name field (first text input)
    cy.get('input[type="text"]').first().type(doctorName);
    cy.wait(1500);
    
    // Email field
    cy.get('input[type="email"]').type(doctorEmail);
    cy.wait(1500);
    
    // Phone field
    cy.get('input[type="tel"]').type(doctorPhone);
    cy.wait(1500);
    
    // Specialization field (last text input)
    cy.get('input[type="text"]').last().type(doctorSpecialization);
    cy.wait(1500);
    
    // Step 9: Select department
    cy.get('select').first().select(1, { force: true });
    cy.wait(1500);
    
    // Step 10: Submit the form
    cy.contains('Oluştur').click();
    cy.wait(3000);
    
    // Step 11: Wait for modal to close and doctor to be added
    cy.contains(doctorName, { timeout: 10000 }).should('be.visible');
    cy.wait(2000);
    cy.contains(doctorEmail).should('be.visible');
    cy.wait(2000);
  });
});

