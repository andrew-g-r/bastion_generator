'use strict';
const form = document.querySelector('#generator');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
let characters = [];
function element(tag, text, className) {
  const item = document.createElement(tag);
  if (text !== undefined) item.textContent = text;
  if (className) item.className = className;
  return item;
}
function display() {
  results.replaceChildren();
  for (const c of characters) {
    const card = element('article');
    card.append(element('h2', c.name), element('h3', c.career));
    const abilities = element('div', undefined, 'abilities');
    ['STR', 'DEX', 'CHA'].forEach((name, i) => abilities.append(element('span', `${name} ${c.abilities[i]}`)));
    abilities.append(element('span', `HP ${c.hp}`), element('span', `£${c.money}`));
    card.append(abilities, element('p', c.description), element('p', c.equipment));
    c.prompts.forEach((prompt, i) => card.append(element('h3', prompt), element('p', c.answers[i])));
    card.append(element('h3', 'Group debt · if youngest'), element('p', c.debt));
    results.append(card);
  }
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  status.textContent = 'Rolling…';
  try {
    const values = new URLSearchParams();
    for (const [key, value] of new FormData(form)) if (value !== '') values.set(key, value);
    values.set('random_name', String(form.elements.random_name.checked));
    const response = await fetch(`/api/generate?${values}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Generation failed');
    characters = data;
    display();
    status.textContent = `${characters.length} character${characters.length === 1 ? '' : 's'} ready.`;
  } catch (error) { status.textContent = error.message; }
  finally { button.disabled = false; }
});
fetch('/api/careers').then(response => response.json()).then(careers => {
  for (const career of careers) {
    const option = element('option', career.title);
    option.value = career.id;
    document.querySelector('#career').append(option);
  }
}).catch(() => { status.textContent = 'Could not load careers. Refresh to try again.'; });
