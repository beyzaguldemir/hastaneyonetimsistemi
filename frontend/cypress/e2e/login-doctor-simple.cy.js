describe('Login and Add Doctor - Simple Test', () => {
  const baseUrl = 'http://localhost:5173';
  const adminEmail = 'admin@hospital.com';
  const adminPassword = 'admin123';

  it('should login and add a new doctor', () => {
    // Giriş yap
    cy.visit(baseUrl);
    cy.wait(3000);
    
    cy.get('input[type="email"]').type(adminEmail);
    cy.wait(2000);
    cy.get('input[type="password"]').type(adminPassword);
    cy.wait(2000);
    cy.get('button[type="submit"]').click();
    cy.wait(3000);
    
    // Dashboard'a yönlendirildiğini kontrol et
    cy.url().should('include', '/dashboard');
    cy.wait(3000);
    
    // Doktorlar sayfasına git
    cy.contains('Doktorlar').click();
    cy.wait(3000);
    
    // Yeni doktor ekle
    cy.contains('+ Yeni Doktor').click();
    cy.wait(2000);
    
    const doctorName = `Dr. Test ${Date.now()}`;
    const doctorEmail = `drtest${Date.now()}@example.com`;
    
    cy.get('input[type="text"]').first().type(doctorName);
    cy.wait(2000);
    cy.get('input[type="email"]').type(doctorEmail);
    cy.wait(2000);
    cy.get('input[type="tel"]').type('05321112233');
    cy.wait(2000);
    cy.get('input[type="text"]').last().type('Kardiyolog');
    cy.wait(2000);
    cy.get('select').first().select(1, { force: true });
    cy.wait(2000);
    
    cy.contains('Oluştur').click();
    cy.wait(4000);
    
    // Doktorun eklendiğini kontrol et
    cy.contains(doctorName, { timeout: 10000 }).should('be.visible');
    cy.wait(3000);
  });
});

