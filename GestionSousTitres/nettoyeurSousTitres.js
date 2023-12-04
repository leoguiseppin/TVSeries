// Importation de modules
const fs = require('fs');
const fse = require('fs-extra');
const AdmZip = require('adm-zip');
const path = require('path');

// Fonction récursive pour parcourir les dossiers
function parcourirDossiers(dossier, dossierErreur) {
  // Liste les fichiers dans le dossier actuel
  const fichiers = fs.readdirSync(dossier);

  // Parcours de chaque fichier
  fichiers.forEach((fichier) => {
    const cheminFichier = `${dossier}/${fichier}`;
    const stat = fs.statSync(cheminFichier);

    if (stat.isDirectory()) {
      // Si le fichier est un répertoire, continuez à parcourir récursivement
      parcourirDossiers(cheminFichier);
    } else {
      if (fichier.endsWith('.zip') || fichier.endsWith('.rar')) {
        try {
          // Extraction du contenu des fichiers ZIP et RAR
          const zip = new AdmZip(cheminFichier);
          zip.extractAllTo(dossier, true);
          // Suppression du fichier d'archive après extraction réussie
          fse.removeSync(cheminFichier);
        } catch (erreur) {
          // Gestion des erreurs lors de la décompression
          console.error(`Erreur lors de la décompression de ${fichier}: ${erreur.message}`);
          const cheminDossierErreur = `${dossierErreur}/${fichier}`;
          // Déplacement du fichier d'archive défectueux vers un dossier d'erreur
          fse.moveSync(cheminFichier, cheminDossierErreur, { overwrite: true });
        }
      }
    }
  });
}

// Chemins des dossiers source et de destination pour le premier parcours
const dossierRacine = 'C:/Users/leogu/Desktop/SAE/sous-titres';
const dossierErreur = 'C:/Users/leogu/Desktop/SAE/undefined';

// Appel de la fonction de parcours pour le premier dossier
parcourirDossiers(dossierRacine, dossierErreur);

// Fonctions pour parcourir les sous-dossiers
function parcourirSousDossiers1(dossier) {
  const sousDossiers1 = fs.readdirSync(dossier);
  sousDossiers1.forEach(sousDossier1 => {
    const sousDossier1Path = path.join(dossier, sousDossier1);
    if (fs.statSync(sousDossier1Path).isDirectory()) {
      parcourirSousDossiers2(sousDossier1Path);
    }
  });
}

function parcourirSousDossiers2(dossier) {
  const sousDossiers2 = fs.readdirSync(dossier);
  sousDossiers2.forEach(sousDossier2 => {
    const sousDossier2Path = path.join(dossier, sousDossier2);
    if (fs.statSync(sousDossier2Path).isDirectory()) {
      if (contientDesFichiers(sousDossier2Path)) {
        deplacerFichiers(sousDossier2Path, dossier);
      }
    }
  });
}

// Vérifier si un dossier contient des fichiers
function contientDesFichiers(dossier) {
  const fichiers = fs.readdirSync(dossier);
  return fichiers.length > 0;
}

// Déplacer des fichiers d'un dossier source vers un dossier de destination
function deplacerFichiers(source, destination) {
  const fichiers = fs.readdirSync(source);
  fichiers.forEach(fichier => {
    const sourcePath = path.join(source, fichier);
    const destinationPath = path.join(destination, fichier);
    fs.renameSync(sourcePath, destinationPath);
  });
  // Supprimer le dossier source une fois les fichiers déplacés
  fs.rmdirSync(source);
}

// Appel des fonctions pour parcourir les sous-dossiers
parcourirSousDossiers1(dossierRacine);

// Appel de la fonction de parcours pour le deuxième dossier
parcourirDossiers(dossierRacine, dossierErreur);

// Fonction pour parcourir les dossiers et gérer les extensions de fichiers
function parcourirDossiers2(dossier, dossierErreur) {
  const fichiers = fs.readdirSync(dossier);

  fichiers.forEach((fichier) => {
    const cheminFichier = path.join(dossier, fichier);
    const stat = fs.statSync(cheminFichier);

    if (stat.isDirectory()) {
      parcourirDossiers2(cheminFichier, dossierErreur);
    } else {
      const extensionsAcceptees = ['.srt', '.vo', '.sub'];
      const derniers4Caracteres = fichier.slice(-4).toLowerCase();

      if (extensionsAcceptees.some(ext => derniers4Caracteres.endsWith(ext))) {
        // Gérer les fichiers avec des extensions acceptées
      } else {
        const destination = path.join(dossierErreur, fichier);

        try {
          // Déplacer les fichiers non acceptés vers le dossier d'erreur
          fs.renameSync(cheminFichier, destination);
        } catch (error) {
          console.error(`Erreur lors du déplacement de ${fichier}: ${error.message}`);
        }
      }
    }
  });
}

// Appel de la fonction de parcours pour le troisième dossier
parcourirDossiers2(dossierRacine, dossierErreur);
