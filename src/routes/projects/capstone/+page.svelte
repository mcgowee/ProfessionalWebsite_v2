<main class="p-8 max-w-5xl mx-auto font-sans text-gray-800 leading-relaxed">
	<div class="mb-12 border-b pb-8">
		<h1 class="text-4xl font-extrabold mb-4 text-blue-900">
			Predictive and Prescriptive Analytics for Behavioral Health Appointment No‑Shows
		</h1>
		<h2 class="text-2xl text-gray-700 font-semibold">
			Capstone Project | MS Data Analytics (AI & ML Specialization)
		</h2>
		<div class="mt-4 text-gray-600 font-medium">
			<span>Earl McGowen</span> • <span>Colorado State University Global</span>
		</div>
	</div>

	<img
		src="/assets/capstone_hero.png"
		alt="Neural network silhouette representing behavioral health analytics"
		class="w-full h-auto rounded-lg shadow-lg mb-12"
	/>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">1. Introduction and Background</h3>
		<p class="mb-4">
			This capstone project focuses on a data‑driven examination of appointment no‑shows within a
			large community mental health organization serving Arapahoe and Douglas counties in Colorado.
			A <em class="font-semibold">no‑show</em> is defined as a scheduled behavioral health appointment
			where the client does not attend and does not cancel within the appropriate time window. No‑shows
			represent a persistent and costly challenge in mental health care, affecting continuity of care,
			operational efficiency, staff workload, and financial sustainability.
		</p>
		<p class="mb-4">
			The organization has identified no‑show reduction as one of its top operational priorities. As
			the data warehouse engineer for this organization, I have received formal approval to use <strong
				class="text-blue-800"
				>fully de‑identified electronic health record (EHR) and data warehouse data</strong
			> for this capstone project. All work is conducted in strict adherence to HIPAA guidelines, with
			ongoing oversight from the organization’s CTO, VP of Technology, and Compliance leadership.
		</p>
		<p>
			This project aligns academic objectives with a real‑world organizational need, providing both
			scholarly rigor and practical impact. By combining traditional data analytics with Artificial
			Intelligence (AI), Machine Learning (ML), and Natural Language Processing (NLP), the project
			aims to uncover previously hidden drivers of appointment non‑attendance and translate them
			into actionable insights.
		</p>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">2. Problem Statement</h3>
		<p class="mb-4">
			High no‑show rates in community mental health settings disrupt care continuity, increase
			administrative burden, and result in lost revenue because Medicaid and most private insurers
			do not reimburse missed appointments. Missed care may also increase the likelihood of crisis
			events, relapse, or clients disengaging from treatment entirely.
		</p>
		<div class="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-600">
			<p class="font-semibold mb-2">
				This capstone addresses the problem by developing an analytics framework that:
			</p>
			<ol class="list-decimal list-inside space-y-2">
				<li>
					<strong>Predicts the risk of no‑shows</strong> for scheduled behavioral health appointments.
				</li>
				<li>
					<strong>Identifies actionable drivers</strong> of no‑show behavior to support operational and
					clinical decision‑making.
				</li>
			</ol>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">3. Business Questions and Hypotheses</h3>

		<div class="grid md:grid-cols-2 gap-8">
			<div>
				<h4 class="text-xl font-semibold mb-3">Business Questions</h4>
				<ul class="list-disc list-inside space-y-2 text-gray-700">
					<li>
						Can independent variables such as transportation barriers, housing instability, and
						social support predict no‑show rates?
					</li>
					<li>
						What factors most strongly influence the likelihood that a client will miss a scheduled
						behavioral health appointment?
					</li>
				</ul>
			</div>

			<div>
				<h4 class="text-xl font-semibold mb-3">Hypotheses</h4>
				<ul class="space-y-4">
					<li class="bg-gray-50 p-4 rounded border border-gray-200">
						<strong class="block mb-1 text-gray-900">Null Hypothesis (H₀):</strong>
						Independent variables (transportation, housing, etc.) do not significantly predict no‑show
						behavior.
					</li>
					<li class="bg-blue-50 p-4 rounded border border-blue-200">
						<strong class="block mb-1 text-blue-900">Alternative Hypothesis (H₁):</strong>
						One or more independent variables significantly predict no‑show behavior at a statistically
						meaningful level.
					</li>
				</ul>
			</div>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">4. Data Sources and Datasets</h3>
		<p class="mb-4">
			All data originates in the organization’s SmartCare EHR and flows into a centralized SQL
			Server data warehouse. The primary dataset consists of <strong
				>924,418 appointment records</strong
			>
			spanning <strong>January 2020 through December 2025</strong>.
		</p>

		<h4 class="text-lg font-bold mt-6 mb-2">Structured Variables</h4>
		<ul class="list-disc list-inside grid md:grid-cols-2 gap-2 text-gray-700 mb-6">
			<li>Appointment attendance (no‑show vs. show)</li>
			<li>Service duration and type</li>
			<li>Program division and location</li>
			<li>Mode of delivery (in‑person vs. telehealth)</li>
			<li>Temporal features (day/hour)</li>
			<li>Limited client demographics</li>
		</ul>

		<h4 class="text-lg font-bold mt-6 mb-2">Temporal Partitioning</h4>
		<div class="flex gap-4">
			<span class="px-3 py-1 bg-gray-200 rounded text-sm font-mono"
				>Training: Jan 2020 – Dec 2023</span
			>
			<span class="px-3 py-1 bg-gray-200 rounded text-sm font-mono">Test: Jan 2024 – Dec 2025</span>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">5. AI, ML, and NLP Feature Engineering</h3>
		<p class="mb-4">
			Mental health care is heavily documentation‑driven, with critical information embedded in
			unstructured clinical notes. To address this, the project incorporates AI and NLP techniques
			to extract privacy‑preserving, interpretable features from de‑identified notes.
		</p>
		<div class="bg-gray-50 p-6 rounded-lg">
			<h4 class="font-bold mb-3">Derived NLP Features</h4>
			<div class="flex flex-wrap gap-2">
				{#each ['Transportation Barriers', 'Housing Instability', 'Social Support', 'Language/Disability', 'Employment Stress', 'Treatment Ambivalence', 'Medication Adherence'] as tag}
					<span class="px-3 py-1 bg-white border border-gray-300 rounded-full text-sm text-gray-700"
						>{tag}</span
					>
				{/each}
			</div>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">6. Modeling Approach</h3>
		<div class="grid md:grid-cols-3 gap-6">
			<div class="border p-4 rounded-lg">
				<h4 class="font-bold text-blue-800 mb-2">Baseline Models</h4>
				<p>Logistic Regression (for interpretability and benchmarking).</p>
			</div>
			<div class="border p-4 rounded-lg">
				<h4 class="font-bold text-blue-800 mb-2">Advanced Models</h4>
				<p>
					Tree‑based classifiers (XGBoost, LightGBM, CatBoost) to capture non‑linear interactions.
				</p>
			</div>
			<div class="border p-4 rounded-lg">
				<h4 class="font-bold text-blue-800 mb-2">Tech Stack</h4>
				<p>Python, pandas, scikit‑learn, Jupyter, Git.</p>
			</div>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">7. Model Evaluation</h3>
		<p class="mb-4">
			Model performance is evaluated using metrics appropriate for imbalanced classification
			problems:
		</p>
		<ul class="list-disc list-inside space-y-1 mb-4">
			<li><strong>ROC‑AUC:</strong> Receiver Operating Characteristic Area Under the Curve</li>
			<li>
				<strong>PR‑AUC:</strong> Precision–Recall Area Under the Curve (Critical for identifying the 10%
				minority class of no-shows)
			</li>
		</ul>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">8. Prescriptive Analytics</h3>
		<p class="mb-4">
			Beyond prediction, this project emphasizes <strong>prescriptive analytics</strong
			>—understanding what interventions work for which client groups.
		</p>
		<ul class="list-disc list-inside space-y-1 text-gray-700">
			<li>Evaluating reminder types (text, call, email)</li>
			<li>Identifying populations that benefit most from telehealth</li>
			<li>Exploring reinforcement learning concepts to assess intervention outcomes over time</li>
		</ul>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">9. Organizational Benefits</h3>
		<div class="grid sm:grid-cols-2 gap-4">
			<div class="bg-green-50 p-4 rounded border border-green-100">
				<h4 class="font-bold text-green-900">Operational Efficiency</h4>
				<p class="text-sm text-green-800">Reduced administrative burden & improved scheduling.</p>
			</div>
			<div class="bg-green-50 p-4 rounded border border-green-100">
				<h4 class="font-bold text-green-900">Clinical Outcomes</h4>
				<p class="text-sm text-green-800">Improved continuity of care & reduced disengagement.</p>
			</div>
			<div class="bg-green-50 p-4 rounded border border-green-100">
				<h4 class="font-bold text-green-900">Financial Impact</h4>
				<p class="text-sm text-green-800">Reduced revenue loss & better resource allocation.</p>
			</div>
			<div class="bg-green-50 p-4 rounded border border-green-100">
				<h4 class="font-bold text-green-900">Innovation & Trust</h4>
				<p class="text-sm text-green-800">Ethical AI application with HIPAA compliance.</p>
			</div>
		</div>
	</section>

	<section class="mb-12">
		<h3 class="text-2xl font-bold mb-4 text-gray-900">10. Ethical and Compliance Considerations</h3>
		<p class="text-gray-700 border-l-4 border-gray-300 pl-4 py-2 bg-gray-50">
			Ethics and privacy are central. All data are de‑identified, access‑controlled, and subject to
			regular leadership review to ensuring patient trust and confidentiality are never compromised.
		</p>
	</section>

	<section class="text-center pt-8 border-t">
		<h3 class="text-xl font-bold mb-4">Conclusion</h3>
		<p class="max-w-3xl mx-auto text-gray-700">
			This capstone integrates predictive and prescriptive analytics to address a critical
			operational and clinical challenge in community mental health care. By combining structured
			data, AI‑assisted feature extraction, and rigorous evaluation, it aims to deliver actionable
			insights that improve care access, efficiency, and outcomes.
		</p>
	</section>
</main>
