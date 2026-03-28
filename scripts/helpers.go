package authgateway

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"fmt"
	"io"
	"log"
	"time"
)

// getPrivateKey returns a new RSA private key.
func getPrivateKey() (*rsa.PrivateKey, error) {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return nil, err
	}
	return privateKey, nil
}

// getCertificate returns a certificate signed by the private key.
func getCertificate(privateKey *rsa.PrivateKey, useExistingCert bool) (*x509.Certificate, error) {
	template := &x509.Certificate{
		SerialNumber: big.NewInt(1),
		NotBefore:    time.Now(),
		NotAfter:     time.Now().AddDate(10, 0, 0),
		KeyUsage:     x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
		ExtKeyUsage:  []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
	}

	if useExistingCert {
		// Assuming we have a function to read the existing cert from disk
		existingCert, err := loadCertificate()
		if err != nil {
			return nil, fmt.Errorf("failed to load existing certificate: %w", err)
		}
		template = existingCert
	} else {
		return template, nil
	}

	return template, privateKey.Sign(rand.Reader, template, []byte{})
}

func loadCertificate() (*x509.Certificate, error) {
	// Implementation to load the existing certificate from disk
	return &x509.Certificate{}, nil
}

func getRandomBytes(size int) ([]byte, error) {
	b := make([]byte, size)
	_, err := io.ReadFull(rand.Reader, b)
	if err != nil {
		return nil, err
	}
	return b, nil
}