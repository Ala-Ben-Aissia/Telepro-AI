# Chapitre V : Implémentation détaillée — Partie Backend

## 1. Présentation générale du backend

Le backend de Telepro-AI a été conçu selon des standards professionnels pour garantir robustesse, sécurité, évolutivité et conformité réglementaire. Il s’appuie sur des patterns éprouvés (modèle MVC, services, repository), une gestion fine des erreurs et des logs, et une intégration continue automatisée.

---

### 1.1. Tableau comparatif des choix technologiques backend

| Critère             | Solution retenue     | Alternatives       | Justification principale          |
| ------------------- | -------------------- | ------------------ | --------------------------------- |
| Framework principal | Django/DRF           | Flask, FastAPI     | Maturité, écosystème, sécurité    |
| Authentification    | JWT (SimpleJWT)      | Session, OAuth2    | Stateless, mobile-friendly        |
| Tâches asynchrones  | Celery + Redis       | RQ, Dramatiq       | Fiabilité, planification, support |
| Base de données     | SQLite               | MySQL, PostgreSQL  | Transactions, JSON, scalabilité   |
| Tests               | Pytest, DRF TestCase | Unittest, Nose     | Expressivité, plugins, coverage   |
| CI/CD               | GitHub Actions       | GitLab CI, Jenkins | Intégration GitHub, simplicité    |

---

Le backend de Telepro-AI repose sur Django 5.1 et Django REST Framework (DRF). Il gère la logique métier, la persistance des données, l’authentification, la gestion des utilisateurs, des patients, des campagnes, l’automatisation (Celery), et intègre une couche IA/ML avancée pour l’analyse et la personnalisation.

---

## 2. Structure et organisation des modules principaux

- **accounts/** : gestion des utilisateurs, authentification (JWT), permissions, sécurité.
- **patients/** : gestion des patients, consentements, préférences, historique médical, anonymisation, migrations.
- **campaigns/** : gestion des campagnes de communication, logs, ciblage, segments, statistiques, migrations.
- **services/** : services métiers, IA/ML (clustering, prédiction, entraînement), gestion d’envoi, tâches Celery.
- **common/** : utilitaires partagés (mixin d’audit, helpers).
- **config/** : configuration Django (settings, urls, asgi, wsgi).
- **logs/**, **backups/**, **example_outputs/** : journaux, sauvegardes, résultats d’expériences ML.

---

## 3. Modélisation des données (extraits et explications)

### a. Modèle Utilisateur (accounts/models.py)

```python
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("STAFF", "Staff"),
        ("PATIENT", "Patient"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="PATIENT")
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    require_password_change = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(default=timezone.now)
```

- Gestion fine des rôles, sécurité renforcée, traçabilité des connexions.

### b. Modèle Patient (patients/models.py)

```python
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    medical_record_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    date_of_birth = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female"), ("O", "Other"), ("N", "Préféré ne pas dire")], null=True, blank=True)
    # ... autres champs : préférences, consentements, anonymisation, etc.
```

- Gestion complète du cycle de vie patient, conformité RGPD, liens avec les consentements et préférences.

### c. Modèle Consentement (patients/models.py)

```python
class ConsentRecord(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="consent_records")
    consent_type = models.CharField(max_length=20, choices=CONSENT_TYPES)
    granted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="recorded_consents")
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    # ...
```

- Traçabilité fine, audit, conformité réglementaire (GDPR).

### d. Modèles Campagne et Logs (campaigns/models.py)

```python
class Campaign(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(CampaignCategory, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    # ... critères de ciblage, templates, etc.

class CommunicationLog(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT)
    communication_type = models.CharField(max_length=10, choices=COMMUNICATION_TYPES)
    status = models.CharField(max_length=20, choices=COMMUNICATION_STATUS, default="PENDING")
    sent_at = models.DateTimeField(null=True)
    # ... autres champs : réponse, erreurs, métadonnées, etc.
```

- Suivi précis des campagnes, logs d’envoi, réponses, erreurs, analyse statistique.

---

## 4. API REST et vues principales (extraits)

### a. Authentification et gestion utilisateur (accounts/views.py)

```python
class PatientRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(user_type="PATIENT")
            refresh = RefreshToken.for_user(user)
            return Response({"message": "Registration successful", ...}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- Inscription, connexion JWT, gestion du profil, changement de mot de passe, logout sécurisé.

### b. Gestion des patients (patients/views.py)

```python
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PatientFilter
    def get_queryset(self):
        user = self.request.user
        if user.user_type == "PATIENT":
            return Patient.objects.filter(user=user)
        return Patient.objects.all()
```

- CRUD patient, filtres avancés, gestion des consentements et préférences via endpoints dédiés.

### c. Gestion des campagnes (campaigns/views.py)

```python
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        """
        Envoi des communications de campagne aux patients ciblés avec consentement actif.
        """
        # ... logique d’envoi
```

- Création, édition, suppression, envoi ciblé, logs, statistiques, recommandations IA.

---

## 5. Sécurité, permissions et conformité

:::tip Bonnes pratiques — Sécurité backend

- Toujours utiliser des variables d’environnement pour les secrets et clés d’API (jamais en dur dans le code).
- Appliquer le principe du moindre privilège sur les permissions (RBAC).
- Activer le logging et l’audit sur toutes les actions sensibles (connexion, modification, suppression).
- Mettre à jour régulièrement les dépendances (pip, Django, DRF) pour éviter les vulnérabilités connues.
- Documenter les politiques de gestion des incidents et des violations de sécurité.
  :::

### 5.1. Approche professionnelle de la sécurité

- Authentification JWT sécurisée (djangorestframework_simplejwt), rotation des tokens, blacklist des refresh tokens.
- Permissions DRF personnalisées (staff, patient, admin), policy-based access control.
- Chiffrement des données sensibles (django-cryptography), gestion des secrets par variables d’environnement.
- Throttling, audit, traçabilité, gestion des erreurs centralisée (Sentry).
- Protection contre les injections SQL, XSS, CSRF, brute-force (limiteurs, validation stricte).

### 5.2. Tableau de synthèse sécurité backend

| Aspect           | Implémentation          | Points forts                | Limites/Perspectives        |
| ---------------- | ----------------------- | --------------------------- | --------------------------- |
| Authentification | JWT, refresh, blacklist | Stateless, scalable         | Nécessite gestion du token  |
| Permissions      | DRF, custom classes     | Granularité, extensible     | Complexité croissante       |
| Chiffrement      | django-cryptography     | RGPD, sécurité au repos     | Overhead possible           |
| Audit/Logs       | Mixins, Sentry          | Traçabilité, alertes        | Analyse avancée à renforcer |
| Throttling       | DRF, custom             | Protection DoS, brute-force | Ajustement fin              |

---

## 6. Tâches asynchrones et automatisation (Celery)

- Exécution en arrière-plan : envoi massif, relances, génération de rapports, analyses ML périodiques
- Planification via Celery Beat

---

## 7. Intelligence Artificielle et Machine Learning (IA/ML)

### a. Objectifs et usages

- Segmentation automatique des patients (clustering KMeans/DBSCAN)
- Prédiction de la réponse des patients aux campagnes (classification, scoring)
- Recommandation de campagnes personnalisées

### b. Pipeline ML (services/ai/)

- **Prétraitement** : extraction, nettoyage, normalisation des données patient et logs de communication
- **Clustering** (clustering.py) : segmentation automatique

```python
class PatientClusteringService:
    @staticmethod
    def cluster_with_dbscan(features, patient_ids, feature_names, eps=None, min_samples=5):
        # ... clustering DBSCAN sur les features patients
```

- **Entraînement et sélection de modèles** (training.py)

```python
def create_ensemble_model(model_type="stacking"):
    rf = RandomForestClassifier(...)
    gb = GradientBoostingClassifier(...)
    et = ExtraTreesClassifier(...)
    if model_type == "voting":
        ensemble = VotingClassifier(...)
    else:
        ensemble = StackingClassifier(...)
    return ensemble

class PatientResponseTrainer:
    def generate_training_data(self, lookback_days=720):
        # ... extraction des features patients + logs, validation, enrichissement
    def train_model(self, ...):
        # ... entraînement, tuning, évaluation, sauvegarde
```

- **Prédiction et recommandation** (prediction.py)

```python
class CampaignPredictionService:
    @staticmethod
    def predict_campaign_effectiveness(campaign_id):
        # ... prédiction du taux de réponse attendu pour une campagne
```

- **Résultats et visualisations** : sauvegarde des modèles (joblib), export CSV/JSON, graphiques d’importance des features, logs d’entraînement

### c. Intégration dans le backend

- Endpoints pour déclencher analyses, récupérer résultats, alimenter la personnalisation côté API
- Utilisation des segments et scores pour le ciblage dynamique des campagnes

---

## Exemples de résultats attendus (IA/ML)

### 1. Segmentation automatique (Clustering)

- **Visualisation des clusters** :  
  Un graphique (ex : scatter plot) montrant la répartition des patients selon deux dimensions principales (âge, score d’engagement), colorés par cluster identifié.
  ![placeholder_cluster](./public/cluster_feature_comparison.png)

- **Tableau de synthèse des segments** :

| Cluster | Nombre de patients | Âge moyen | Score d’engagement moyen | Langue dominante | Taux de réponse (%) |
| ------- | ------------------ | --------- | ------------------------ | ---------------- | ------------------- |
| 0       | 150                | 34        | 0.82                     | Français         | 48                  |
| 1       | 120                | 55        | 0.66                     | Arabe            | 35                  |
| 2       | 90                 | 28        | 0.90                     | Français         | 62                  |

---

### 2. Importance des variables (Feature importance)

- **Graphique d’importance** :  
  ![placeholder_importance](./public/feature_importance.png)

- **Exemple de top features** :

| Rang | Variable                  | Importance (%) |
| ---- | ------------------------- | -------------- |
| 1    | engagement_score          | 26             |
| 2    | recent_response_rate      | 17             |
| 3    | age_group                 | 13             |
| 4    | preferred_contact_methods | 10             |
| 5    | matches_language          | 8              |

---

### 3. Prédiction de la réponse aux campagnes

- **Rapport de performance du modèle** :

  - Accuracy : 0.81
  - ROC AUC : 0.87
  - Precision : 0.79
  - Recall : 0.76
  - Courbe ROC et matrice de confusion (à insérer en annexe ou via un placeholder image)

- **Exemple de prédiction individuelle** :

| Patient ID | Probabilité de réponse (%) | Segment | Action recommandée       |
| ---------- | -------------------------- | ------- | ------------------------ |
| 4e2f...    | 92                         | 2       | Envoyer SMS personnalisé |
| 7b1c...    | 38                         | 1       | Relance par email        |
| 9d5a...    | 61                         | 0       | Appel téléphonique       |

---

### 4. Recommandations opérationnelles

- **Liste des patients à relancer** (extrait) :

| Patient       | Dernier contact | Score d’engagement | Risque d’inactivité | Action      |
| ------------- | --------------- | ------------------ | ------------------- | ----------- |
| M. Ben Ali    | 2025-04-12      | 0.32               | Élevé               | Relance SMS |
| Mme. Trabelsi | 2025-03-28      | 0.54               | Moyen               | Email       |

- **Statistiques globales** :
  - % de patients segmentés automatiquement : 100%
  - % de campagnes bénéficiant d’une recommandation IA : 85%
  - Gain de taux de réponse estimé grâce à la personnalisation : +22%

---

### 5. Export de résultats (fichiers générés)

- `patient_clusters.json` : Affectation de chaque patient à un cluster.
- `feature_importance.csv` : Poids de chaque variable dans la prédiction.
- `patient_response_model.joblib` : Modèle ML sauvegardé.
- `patient_statistics.json` : Statistiques agrégées sur les patients, segments, campagnes.

---

## 8. Sauvegardes, logs et outils annexes

- Exports réguliers de la base (backups/)
- Journaux d’exécution (logs/)
- Résultats d’expériences et modèles ML (example_outputs/)

---

## 9. Robustesse, tests et CI/CD backend

:::tip Bonnes pratiques — Robustesse & Tests backend

- Rédiger des tests unitaires pour chaque modèle, vue, service métier.
- Couvrir les cas d’erreur et de bord dans les tests (inputs invalides, permissions, exceptions).
- Utiliser le mocking pour isoler les dépendances externes (APIs, tâches Celery).
- Maintenir une couverture de code >80% pour garantir la fiabilité.
- Intégrer les tests dans le pipeline CI/CD pour éviter toute régression en production.
  :::

### 9.1. Stratégie de robustesse

- Gestion centralisée des exceptions (custom exception handlers)
- Validation stricte des entrées (serializers, schémas)
- Monitoring (Sentry, logs structurés)
- Rollback automatique en cas d’échec critique

### 9.2. Tests automatisés

- Couverture élevée via Pytest et DRF TestCase
- Tests unitaires sur modèles, vues, services
- Tests d’intégration sur endpoints critiques
- Mocking des tâches Celery et des appels externes

### 9.3. CI/CD

- Pipeline GitHub Actions : lint (flake8), tests, build, migrations, déploiement staging/prod
- Déploiement automatisé sur serveur sécurisé (Docker, Gunicorn, Nginx)

## 10. Schémas et diagrammes (placeholders)

- MCD/MLD (patients, users, campaigns, logs…)
- Diagramme de classes Django
- Diagramme de séquence (ex : pipeline ML, envoi de campagne)
- Architecture globale (backend, frontend, ML, base de données)

---

_La section backend est ainsi couverte de manière exhaustive, avec un accent particulier sur la partie IA/ML et la personnalisation intelligente du système._

# Chapitre VI : Implémentation détaillée — Partie Frontend

:::tip Bonnes pratiques — Développement frontend

- Utiliser des composants réutilisables et typés (TypeScript) pour limiter la duplication.
- Privilégier la composition (props.children, hooks) à l’héritage.
- Factoriser la logique métier côté client dans des hooks personnalisés (`/hooks`).
- Documenter les composants complexes avec des exemples d’utilisation (Storybook recommandé).
- Organiser le code selon l’atomic design pour la maintenabilité.
  :::

## 1. Présentation générale du frontend

Le frontend de Telepro-AI est pensé selon les standards modernes : modularité, accessibilité, UX centrée utilisateur, sécurité et maintenabilité. Il adopte une architecture scalable, des patterns avancés (atomic design, hooks, context providers) et une intégration continue.

---

### 1.1. Tableau comparatif des choix technologiques frontend

| Critère             | Solution retenue       | Alternatives           | Justification principale       |
| ------------------- | ---------------------- | ---------------------- | ------------------------------ |
| Framework principal | Next.js 15             | CRA, Gatsby, Nuxt      | SSR/CSR, performance, DX       |
| UI & styles         | Tailwind CSS, Radix    | Chakra, MUI, Styled    | Rapidité, accessibilité, thème |
| Icons               | Lucide React           | Heroicons, FontAwesome | Cohérence, modernité           |
| State/API           | SWR, React Context     | Redux, React Query     | Simplicité, perf, SSR          |
| Validation          | Zod, React Hook Form   | Yup, Formik            | Typescript natif, robustesse   |
| Tests               | Jest, RTL, Cypress     | Vitest, Playwright     | Complémentarité, maturité      |
| CI/CD               | Vercel, GitHub Actions | Netlify, Jenkins       | Intégration Next.js, preview   |

---

Le frontend de Telepro-AI est développé avec Next.js 15 et React 19, en TypeScript. Il offre une expérience utilisateur moderne, responsive et sécurisée, adaptée aux besoins des patients comme des professionnels de santé. L’interface met l’accent sur la gestion des consentements, la personnalisation, l’accessibilité et la cohérence visuelle.

---

## 2. Architecture et organisation du code

- **/app/** : structure App Router Next.js (pages, layout, server actions)
- **/components/** : composants UI réutilisables (cards, forms, modals, tables, notifications)
- **/hooks/** : hooks personnalisés pour la gestion d’état, l’intégration API, la sécurité
- **/lib/** : helpers, validation, logique métier côté client
- **/styles/** : configuration Tailwind CSS, thèmes, variables de design
- **/public/** : assets, images, icônes

---

## 3. Design system et expérience utilisateur

- **Palette** : bleu/indigo moderne, accessible, cohérente sur toutes les pages
- **Typographie** : hiérarchie claire, police lisible, tailles adaptées
- **Icônes** : Lucide React, intégration harmonieuse dans les composants
- **Composants** : cards à barres d’accent dégradées, formulaires aérés, feedback visuel (états de chargement, succès, erreurs)
- **Accessibilité** : contrastes respectés, navigation clavier, labels explicites, ARIA

---

## 4. Pages et parcours utilisateur principaux

### a. Portail patient (`/app/patients/[id]/portal/page.tsx`)

- **Gestion du consentement global** (toggle `has_active_consent`)
- **Vérification de sécurité** (modal lors de changements critiques)
- **Gestion détaillée des consentements individuels** (tableau, switches, historique)
- **Préférences de communication** (langue, méthode, créneaux horaires, notifications)
- **Feedback utilisateur** (messages de succès, erreurs, loaders)
- **Exemple de composant** :

```tsx
<Card>
  <div className="flex items-center justify-between">
    <span className="font-bold">Consentement général</span>
    <Switch checked={hasActiveConsent} onChange={toggleConsent} />
  </div>
  <ConsentDetailsTable consents={individualConsents} />
</Card>
```

### b. Tableau de bord professionnel (`/app/dashboard/page.tsx`)

- Vue synthétique des patients, campagnes, consentements
- Accès rapide aux actions clés (création campagne, export, analyse)

### c. Création et gestion de campagnes (`/app/campaigns/*`)

- Formulaires multi-étapes, sélection de segments, templates dynamiques
- Visualisation des statistiques de campagne (graphiques, taux de réponse)

---

## 5. Gestion d’état, intégration API et sécurité

- **Gestion d’état** : SWR pour la synchronisation côté client/serveur, React Hook Form pour la validation
- **API** : appels sécurisés aux endpoints Django DRF (authentification JWT, refresh token, gestion des erreurs)
- **Sécurité** : vérification d’authentification sur chaque page sensible, gestion des rôles (admin, patient), protection contre les attaques XSS/CSRF
- **Validation** : schémas Zod côté client pour la robustesse des formulaires

---

## 6. Accessibilité et responsive design

- **Responsive** : layout adaptatif (mobile, tablette, desktop), grille CSS, composants fluides
- **Accessibilité** : navigation clavier, focus visible, annonces ARIA pour les feedbacks

---

## 7. Exemples de code clés

### a. Hook personnalisé pour l’intégration API

```tsx
import useSWR from 'swr'
import { fetcher } from '@/lib/fetcher'

export function usePatientData(patientId: string) {
  const { data, error, isLoading } = useSWR(
    `/api/patients/${patientId}/`,
    fetcher
  )
  return { data, error, isLoading }
}
```

### b. Validation avancée de formulaire

```tsx
import { z } from 'zod'

export const ConsentFormSchema = z.object({
  has_active_consent: z.boolean(),
  communication_preferences: z.object({
    language: z.string(),
    methods: z.array(z.string()),
    time_of_day: z.string(),
    notifications: z.object({
      sms: z.boolean(),
      email: z.boolean(),
      in_app: z.boolean(),
    }),
  }),
})
```

### c. Exemple d’état de chargement et de feedback utilisateur

```tsx
;<Button disabled={isLoading}>
  {isLoading ? <LoaderIcon /> : 'Enregistrer'}
</Button>
{
  success && (
    <Alert
      type="success"
      message="Préférences enregistrées avec succès"
    />
  )
}
```

---

## 8. Robustesse, sécurité et tests frontend

:::tip Bonnes pratiques — Robustesse & Sécurité frontend

- Toujours valider les données côté client (Zod, RHF) avant envoi à l’API.
- Afficher des messages d’erreur clairs et contextualisés à l’utilisateur.
- Utiliser des ErrorBoundary pour éviter les crashs globaux de l’application.
- Ne jamais exposer de données sensibles dans le code ou le stockage local.
- Vérifier systématiquement l’authentification et les droits d’accès sur chaque page.
  :::

### 8.1. Robustesse et gestion des erreurs

- Gestion centralisée des erreurs via ErrorBoundary et hooks personnalisés (useErrorHandler)
- Feedback utilisateur systématique (loaders, alertes, toasts)
- Validation stricte des formulaires (Zod, React Hook Form)

### 8.2. Sécurité côté interface

- Vérification du JWT et des rôles à chaque navigation sensible (guards, context)
- Protection XSS/CSRF (sanitization, cookies httpOnly, headers sécurisés)
- Masquage des informations sensibles côté client

### 8.3. Tests et CI/CD

- Tests unitaires (Jest, React Testing Library) sur composants, hooks, pages
- Tests end-to-end (Cypress) sur parcours critiques (consentement, profil, campagnes)
- Pipeline CI/CD Vercel : lint, build, preview, déploiement automatique

---

## 9. Architecture avancée, UX et évolutivité

:::tip Bonnes pratiques — UX & Accessibilité

- Respecter les contrastes couleurs (AA/AAA) et la hiérarchie visuelle.
- Rendre tous les éléments interactifs accessibles au clavier et aux lecteurs d’écran.
- Fournir un feedback immédiat lors des actions utilisateur (chargement, succès, erreur).
- Tester l’interface sur plusieurs tailles d’écran et appareils.
- Utiliser les icônes et couleurs de façon cohérente pour guider l’utilisateur.
  :::

### 9.1. Architecture scalable

- Découpage atomic design (atoms, molecules, organisms)
- Utilisation de context providers pour la gestion globale (auth, thème, notifications)
- Lazy loading, code splitting, optimisation SSR/ISR

### 9.2. Expérience utilisateur professionnelle

- Parcours utilisateurs testés (personas, wireframes, tests UX)
- Accessibilité renforcée (navigation clavier, ARIA, contrastes, focus visibles)
- Personnalisation dynamique (affichage selon rôle, préférences, langue)

### 9.3. Tableau comparatif patterns frontend

| Aspect      | Implémentation Telepro-AI | Alternatives             | Avantages principaux         |
| ----------- | ------------------------- | ------------------------ | ---------------------------- |
| State/API   | SWR, Context, hooks       | Redux, MobX, React Query | Simplicité, perf, SSR        |
| UI/Design   | Tailwind, Radix, Lucide   | MUI, AntD, Styled        | Accessibilité, custom facile |
| Validation  | Zod, React Hook Form      | Yup, Formik              | Typesafe, DX, robustesse     |
| Tests       | Jest, RTL, Cypress        | Playwright, Vitest       | Complémentarité, rapidité    |
| Auth/Guards | Context, hooks, guards    | HOC, Redux middleware    | Granularité, flexibilité     |

---

- Amélioration continue de l’accessibilité et de l’UX
- Ajout de fonctionnalités temps réel (WebSocket, notifications push)
- Internationalisation complète (i18n)
- Version mobile native (React Native)
- Intégration de modules analytics avancés

---

# Chapitre VII : Prototype matériel — passerelle IoT ESP32 TTGO T-Call (SIM800L)

## 1. Objectif et intégration dans la solution Telepro-AI

Ce prototype matériel a été conçu pour servir de passerelle IoT entre la plateforme Telepro-AI et les patients, notamment ceux ne disposant pas de smartphone ou d’accès Internet fiable. Il permet :

- L’envoi de SMS personnalisés (rappels, notifications santé)
- La réalisation d’appels automatisés (fonctionnalité de base déjà opérationnelle, extension future prévue avec NLP pour répondeur intelligent)
- La validation terrain de la chaîne de communication patient (hardware + API)

## 2. Architecture matérielle et logicielle

- **Carte** : ESP32 TTGO T-Call (modem SIM800L intégré)
- **Périphériques** : buzzer (feedback sonore), modem GSM, alimentation LiPo
- **Librairies principales** : TinyGSM, ArduinoJson, WiFi, HTTPClient
- **Fonctionnalités logicielles** :
  - Connexion WiFi sécurisée (timeout, retry)
  - Initialisation et contrôle du modem SIM800L (AT commands)
  - Authentification sur l’API Django (endpoint `/api/accounts/token/`)
  - Envoi de SMS via endpoint REST (`/api/campaigns/analytics/test-sms/`)
  - Appels vocaux (gestion du timeout, feedback buzzer)
  - Gestion des erreurs, feedback utilisateur (buzzer, logs série)
  - Structure Patient pour personnalisation des messages

**Schéma d’architecture simplifié :**

```
[Telepro-AI API] <---WiFi---> [ESP32 TTGO T-Call] <---GSM---> [Patient]
                                        |
                                   [Buzzer]
```

## 3. Extrait de code clé — Contact patient

```cpp
struct Patient {
  String username;
  String password;
  String phone_number;
  String uuid;
  String preferred_contact_methods;
};

String contactPatient(const String &authToken, const String &recipientNumber, const String &contactMethod) {
  // Authentification, requête HTTP, gestion du retour, feedback buzzer
}
```

## 4. Cas d’usage et résultats

- **Envoi de SMS personnalisé** : test réussi sur plusieurs numéros, réception instantanée, logs côté API.
- **Appel vocal** : connexion, gestion du décrochage, feedback sonore (buzzer), logs côté hardware.
- **Robustesse** : gestion automatique des erreurs réseau, reconnexion, retries, indication sonore en cas d’échec.

## 5. Perspectives d’évolution

- **Répondeur automatique intelligent** : intégration future d’un module NLP embarqué (reconnaissance de mots-clés, réponses automatiques, orientation patient)
- **Intégration temps réel avec Telepro-AI** : synchronisation des campagnes, remontée des statuts d’envoi, logs centralisés
- **Sécurité** : chiffrement des communications, gestion des accès SIM
- **Scalabilité** : déploiement multi-dispositifs (pour patients sans smartphone)

## 6. Schémas, composants et photos (placeholders)

- **Schéma de câblage** : _(placeholder — à insérer)_
- **Liste des composants** : _(placeholder — à compléter)_
- **Photos du montage réel** : _(placeholder — à insérer)_

## 7. Tableau comparatif — TTGO T-Call vs ESP32 + SIM800L séparés

| Critère                 | TTGO T-Call (ESP32 + SIM800L intégré) |         ESP32 + SIM800L séparés         |
| ----------------------- | :-----------------------------------: | :-------------------------------------: |
| Intégration matérielle  |          Tout-en-un, compact          |     Modules séparés, câblage manuel     |
| Facilité de prototypage |     Très simple, moins d’erreurs      | Plus complexe, risques de faux contacts |
| Consommation énergie    |   Optimisée (alimentation partagée)   |         Variable selon montage          |
| Stabilité               |         Bonne (moins de fils)         |         Peut être moins stable          |
| Coût                    |         Légèrement supérieur          |           Parfois moins cher            |
| Disponibilité           |             Très répandue             | Modules parfois plus faciles à trouver  |
| Support communauté      |    Large (doc, tutos spécifiques)     |        Large (plus généraliste)         |
| Évolutivité             |          Limitée à la carte           |    Plus flexible (choix composants)     |

:::tip Bonnes pratiques — Prototypage IoT santé

- Séparer la logique de communication (GSM) et la logique applicative (API, gestion patient)
- Prévoir des timeouts/retries pour la connectivité réseau
- Protéger les informations sensibles (numéros, tokens) en mémoire et sur le réseau
- Utiliser un feedback utilisateur clair (buzzer, LED, logs) pour chaque étape critique
- Prévoir l’évolutivité (OTA, logs distants, diagnostics)
  :::

---

# Annexe : Extraits d’interfaces et diagrammes (placeholders)

- Capture d’écran du portail patient
- Diagramme de navigation Next.js
- Extrait de composant ConsentForm
- Architecture frontend globale
