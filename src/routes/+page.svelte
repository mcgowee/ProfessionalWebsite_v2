<script lang="ts">
  import Conversion from '../components/Conversion.svelte';
  import Hero from '../components/Hero.svelte';
  import Service from '../components/Service.svelte';

  // Keeping these imports commented until you re-enable those sections:
  // import FaQs from '../components/FAQs.svelte';
  // import Reviews from '../components/Reviews.svelte';
</script>

<section class="intro">
  <img class="headshot" src="/headshot.jpg" alt="Earl Leonard McGowen IV" />

  <div class="introText">
    <h1 class="introTitle">Welcome to My Professional Site</h1>
    <p class="introBody">
      Hi, I&apos;m Earl Leonard McGowen IV, a seasoned database programmer, legal analyst, and AI enthusiast with over
      15 years of experience in database programming and architecture. I specialize in creating innovative solutions
      using cutting-edge technologies. Explore my site to learn more about my work and expertise.
    </p>
  </div>
</section>

<main class="main">
  <Hero />

  <Service />
  <!--
  <Reviews />
  <FaQs />
  -->
  
  <Conversion />

</main>

<style>
  .intro {
    margin-top: 22px;
    padding: 18px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);

    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 18px;
    align-items: center;
  }

  .headshot {
    width: 140px;
    height: 140px;
    object-fit: cover;
    border-radius: 999px;
    border: 4px solid var(--brand);
    box-shadow: var(--shadow-sm);
  }

  .introTitle {
    margin: 0 0 10px;
    font-size: 28px;
    line-height: 1.15;
    letter-spacing: -0.01em;
  }

  .introBody {
    margin: 0;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.6;
  }

  .main {
    margin-top: 18px;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  @media (max-width: 720px) {
    .intro {
      grid-template-columns: 1fr;
      text-align: left;
    }

    .headshot {
      width: 110px;
      height: 110px;
    }
  }
</style>
