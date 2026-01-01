<script>
  import '../app.css';
  import Header from '../components/Header.svelte';

  const title = 'Earl McGowen Colorado - AI, Data Analytics, and SQL Expert';
  const description =
    'Earl McGowen from Colorado is a seasoned expert in AI, Data Analytics, and SQL, providing top-notch services and insights.';
  const keywords =
    'Earl McGowen, Colorado, AI, Data Analytics, SQL, AI Expert, Data Analytics Expert, SQL Expert';

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: 'Earl McGowen',
    jobTitle: 'AI, Data Analytics, and SQL Expert',
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'Aurora',
      addressRegion: 'Colorado',
      addressCountry: 'USA'
    },
    description,
    url: 'https://earl-mcgowen.com/'
  };
</script>

<svelte:head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta name="keywords" content={keywords} />
  <script type="application/ld+json">{JSON.stringify(structuredData)}</script>
</svelte:head>

<Header />
<main class="container">
  <slot />
</main>
