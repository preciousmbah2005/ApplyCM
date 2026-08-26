<script lang="ts">
  let firstName = $state("");
  let lastName = $state("");
  let phone = $state("");
  let email = $state("");

  async function handleSubmit() {
    const res = await fetch("http://localhost:8001/api/v1/student-profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstName,
        lastName,
        phone,
        email,
      }),
    });
    const data = await res.json();
    console.log(data);
  }
</script>

<div class="step-page">
  <h3 class="step-title">Personal Details</h3>
  <form onsubmit={(e) => e.preventDefault()}>
    <input type="text" placeholder="First Name" required />
    <input type="text" placeholder="Last Name" required />
    <input type="tel" placeholder="Phone Number" required />
    <button type="submit" class="btn-save">Save & Continue</button>
  </form>
</div>

<style>
  .step-page {
    text-align: left;
  }
  .btn-save {
    margin-top: 2rem;
    padding: 0.5rem 1rem;
    background-color: #3182ce;
    color: white;
    font-size: 1rem;
    border: none;
    width: fit-content;
    border-radius: 50px;
    cursor: pointer;
  }
  .btn-save:hover {
    padding-top: 1rem;
    transition: all 0.2s ease-in-out;
  }
  .step-title {
    margin-bottom: 2rem;
    font-size: 2rem;
    font-weight: 700;
    color: #2d3748;
  }
  .step-page form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .step-page form input {
    padding: 0.5rem 1rem;
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    font-size: 1rem;
  }
</style>
