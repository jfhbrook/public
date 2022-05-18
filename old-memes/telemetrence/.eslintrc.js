module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  extends: ['plugin:@typescript-eslint/recommended', 'plugin:prettier/recommended'],
  ignorePatterns: ['target/', 'boltzmann.js', 'boltzmann.d.ts'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { varsIgnorePattern: '(_|Context)', argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-var-requires': [0],
  },
}
