describe('Hospital Management System E2E Tests', () => {
  const baseUrl = 'http://localhost:5173';
  const adminEmail = 'admin@hospital.com';
  const adminPassword = 'admin123';

  beforeEach(() => {
    // Visit the application
    cy.visit(baseUrl);
  });

  it('should open the site and login with admin user', () => {
    // Verify we're on the login page
    cy.url().should('include', '/login');
    cy.wait(1000); // Wait for page to load
    cy.contains('Hastane Yönetim Sistemi').should('be.visible');
    cy.wait(500);
    
    // Fill in login form
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(500);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(500);
    
    // Submit login form
    cy.get('button[type="submit"]').click();
    cy.wait(1000);
    
    // Wait for redirect to dashboard
    cy.url().should('include', '/dashboard');
    cy.wait(1000);
    cy.contains('Dashboard').should('be.visible');
    cy.wait(1000);
  });

  it('should navigate to Patients page and add a new patient', () => {
    // Login first
    cy.visit(baseUrl);
    cy.wait(1000);
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(500);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(500);
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
    
    // Wait for dashboard to load
    cy.url().should('include', '/dashboard');
    cy.wait(1000);
    
    // Navigate to Patients page
    cy.contains('Hastalar').click();
    cy.wait(1000);
    cy.url().should('include', '/patients');
    cy.wait(1000);
    cy.contains('Hastalar').should('be.visible');
    cy.wait(500);
    
    // Click on "Yeni Hasta" button
    cy.contains('+ Yeni Hasta').click();
    cy.wait(1000);
    
    // Fill in patient form
    const patientName = `Test Patient ${Date.now()}`;
    const patientEmail = `testpatient${Date.now()}@example.com`;
    const patientPhone = '05321111111';
    const patientBirthDate = '1990-01-01';
    const patientAddress = 'Test Address, Istanbul';
    
    cy.get('input[type="text"]').first().type(patientName);
    cy.wait(500);
    cy.get('input[type="email"]').type(patientEmail);
    cy.wait(500);
    cy.get('input[type="tel"]').type(patientPhone);
    cy.wait(500);
    cy.get('input[type="date"]').type(patientBirthDate);
    cy.wait(500);
    cy.get('textarea').first().type(patientAddress);
    cy.wait(500);
    
    // Submit the form
    cy.contains('Oluştur').click();
    cy.wait(2000);
    
    // Wait for modal to close and patient to be added
    cy.contains(patientName, { timeout: 10000 }).should('be.visible');
    cy.wait(1000);
    cy.contains(patientEmail).should('be.visible');
    cy.wait(1000);
  });

  it('should navigate to Departments page and add a new department', () => {
    // Login first
    cy.visit(baseUrl);
    cy.wait(1000);
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(500);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(500);
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
    
    // Wait for dashboard to load
    cy.url().should('include', '/dashboard');
    cy.wait(1000);
    
    // Navigate to Departments page
    cy.contains('Departmanlar').click();
    cy.wait(1000);
    cy.url().should('include', '/departments');
    cy.wait(1000);
    cy.contains('Departmanlar').should('be.visible');
    cy.wait(500);
    
    // Click on "Yeni Departman" button
    cy.contains('+ Yeni Departman').click();
    cy.wait(1000);
    
    // Fill in department form
    const departmentName = `Test Department ${Date.now()}`;
    const departmentDescription = 'This is a test department created by Cypress E2E test';
    
    cy.get('input[type="text"]').first().type(departmentName);
    cy.wait(500);
    cy.get('textarea').first().type(departmentDescription);
    cy.wait(500);
    
    // Submit the form
    cy.contains('Oluştur').click();
    cy.wait(2000);
    
    // Wait for modal to close and department to be added
    cy.contains(departmentName, { timeout: 10000 }).should('be.visible');
    cy.wait(1000);
    cy.contains(departmentDescription).should('be.visible');
    cy.wait(1000);
  });

  it('should complete full workflow: login -> add patient -> add department', () => {
    // Step 1: Login
    cy.visit(baseUrl);
    cy.wait(1000);
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(500);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(500);
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
    cy.url().should('include', '/dashboard');
    cy.wait(1000);
    
    // Step 2: Add a new patient
    cy.contains('Hastalar').click();
    cy.wait(1000);
    cy.url().should('include', '/patients');
    cy.wait(1000);
    cy.contains('+ Yeni Hasta').click();
    cy.wait(1000);
    
    const patientName = `Full Test Patient ${Date.now()}`;
    const patientEmail = `fulltest${Date.now()}@example.com`;
    
    cy.get('input[type="text"]').first().type(patientName);
    cy.wait(500);
    cy.get('input[type="email"]').type(patientEmail);
    cy.wait(500);
    cy.get('input[type="tel"]').type('05329999999');
    cy.wait(500);
    cy.get('input[type="date"]').type('1985-05-15');
    cy.wait(500);
    cy.get('textarea').first().type('Full test address');
    cy.wait(500);
    
    cy.contains('Oluştur').click();
    cy.wait(2000);
    cy.contains(patientName, { timeout: 10000 }).should('be.visible');
    cy.wait(1000);
    
    // Step 3: Add a new department
    cy.contains('Departmanlar').click();
    cy.wait(1000);
    cy.url().should('include', '/departments');
    cy.wait(1000);
    cy.contains('+ Yeni Departman').click();
    cy.wait(1000);
    
    const departmentName = `Full Test Department ${Date.now()}`;
    
    cy.get('input[type="text"]').first().type(departmentName);
    cy.wait(500);
    cy.get('textarea').first().type('Full test department description');
    cy.wait(500);
    
    cy.contains('Oluştur').click();
    cy.wait(2000);
    cy.contains(departmentName, { timeout: 10000 }).should('be.visible');
    cy.wait(1000);
  });
});
