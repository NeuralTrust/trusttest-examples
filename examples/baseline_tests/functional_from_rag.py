"""Baseline test for functional RAG evaluation using RAGProbe with different benign question types in French."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CompletenessEvaluator,
    CorrectnessEvaluator,
    ToneEvaluator,
)
from trusttest.knowledge_base import Document, InMemoryKnowledgeBase
from trusttest.probes.rag import BenignQuestion, RAGProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

documents = [
    Document(
        id="1",
        content="""
        TYPES DE COMPTES:
        - Comptes chèques: Sans frais mensuels avec dépôt direct, sinon 12$/mois
        - Comptes épargne: 0,05% TAP, solde minimum 100$
        - Marché monétaire: 0,10% TAP, solde minimum 2 500$
        - Certificats de dépôt: 0,25% TAP pour 12 mois, 0,50% TAP pour 24 mois
        - Comptes commerciaux: Structure tarifaire séparée, contactez la banque commerciale
        """.strip(),
        topic="Types de comptes",
    ),
    Document(
        id="2",
        content="""
        SERVICES BANCAIRES EN LIGNE ET MOBILES:
        - Services bancaires en ligne: Gratuit, disponible 24h/24 et 7j/7
        - Application mobile: Gratuite, prend en charge le dépôt de chèques et le paiement de factures
        - Paiement de factures: Gratuit pour 10 paiements/mois, 0,50$ chacun après
        - Zelle: Virements gratuits vers d'autres banques
        - Alertes: Alertes gratuites de solde et de transactions
        """.strip(),
        topic="Services bancaires en ligne et mobiles",
    ),
    Document(
        id="3",
        content="""
        CARTES DE DÉBIT ET DE CRÉDIT:
        - Cartes de débit: Gratuites avec compte chèques, frais de remplacement 5$
        - Cartes de crédit: TAP d'introduction 0% pendant 12 mois, 15,99% variable après
        - Récompenses: 1% de remise en argent sur tous les achats
        - Protection contre la fraude: Responsabilité zéro pour les frais non autorisés
        - Frais internationaux: 3% de frais de transaction étrangère
        """.strip(),
        topic="Cartes de débit et de crédit",
    ),
    Document(
        id="4",
        content="""
        PRÊTS ET CRÉDITS:
        - Prêts personnels: TAP 7,99%, 1 000$ à 50 000$
        - Prêts automobiles: TAP 4,99% pour les voitures neuves, 5,99% pour les occasions
        - Prêts immobiliers: TAP 6,5% pour 30 ans fixe, 6,0% pour 15 ans
        - Prêts commerciaux: Contactez la banque commerciale pour les taux
        - Lignes de crédit: Disponibles pour les clients qualifiés
        """.strip(),
        topic="Prêts et crédits",
    ),
    Document(
        id="5",
        content="""
        SERVICES D'INVESTISSEMENT:
        - Comptes d'investissement: Minimum 25$ pour ouvrir
        - Fonds communs de placement: Fonds sans frais d'entrée disponibles
        - Comptes de retraite: IRA traditionnels et Roth
        - Planification financière: Consultation gratuite pour les titulaires de compte
        - Transferts 401(k): Assistance gratuite disponible
        """.strip(),
        topic="Services d'investissement",
    ),
    Document(
        id="6",
        content="""
        SÉCURITÉ ET FRAUDE:
        - Authentification à deux facteurs: Requise pour les services bancaires en ligne
        - Surveillance de la fraude: Surveillance du compte 24h/24 et 7j/7
        - Protection contre le vol d'identité: Disponible pour 9,99$/mois
        - Verrouillage de compte: Disponible via l'application mobile
        - Notifications de voyage: Requises pour l'utilisation internationale de la carte
        """.strip(),
        topic="Sécurité et fraude",
    ),
    Document(
        id="7",
        content="""
        SERVICE CLIENTÈLE:
        - Support téléphonique: 24h/24 et 7j/7 au 1-800-TRUSTBANK
        - Heures des succursales: Lundi-Vendredi 9h-17h, Samedi 9h-13h
        - Réseau de GAB: Plus de 50 000 emplacements à l'échelle nationale
        - Devises étrangères: Disponibles dans certaines succursales
        - Services de notaire: Gratuits pour les titulaires de compte
        """.strip(),
        topic="Service clientèle",
    ),
]


target = HttpTarget(
    url="https://my-llm/chat_french",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        rate_limit=1,
        timeout=60,
        format={
            "message": "{{ test }}",
        },
    ),
    concatenate_field="response",
)


for question_type in BenignQuestion:
    knowledge_base = InMemoryKnowledgeBase(documents=documents)
    probe = RAGProbe(
        target=target,
        knowledge_base=knowledge_base,
        num_questions=5,
        question_types=[question_type],
        language="French",
    )

    question_type_name = question_type.value.replace("_", " ").title()
    scenario = EvaluationScenario(
        name=f"Functional: RAG {question_type_name}",
        description=f"Test scenario for functional RAG {question_type_name}",
        evaluator_suite=EvaluatorSuite(
            evaluators=[
                CorrectnessEvaluator(),
                ToneEvaluator(),
                CompletenessEvaluator(),
            ],
            criteria="any_fail",
        ),
        category="functional",
        type="question-answer",
    )

    test_set = probe.get_test_set()
    results = scenario.evaluate(test_set)
    results.display_summary()

    client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTURST_TOKEN"))

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
