import { describe, it, expect, beforeEach } from 'vitest';
import { storage } from './storage';

describe('storage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should set and get item', () => {
    const testData = { name: 'test', value: 123 };
    storage.set('test', testData);
    
    const result = storage.get('test');
    expect(result).toEqual(testData);
  });

  it('should return null for non-existent key', () => {
    const result = storage.get('nonexistent');
    expect(result).toBeNull();
  });

  it('should remove item', () => {
    storage.set('test', 'value');
    storage.remove('test');
    
    const result = storage.get('test');
    expect(result).toBeNull();
  });

  it('should clear all items with prefix', () => {
    storage.set('key1', 'value1');
    storage.set('key2', 'value2');
    storage.clear();
    
    expect(storage.get('key1')).toBeNull();
    expect(storage.get('key2')).toBeNull();
  });

  it('should handle JSON parse errors gracefully', () => {
    localStorage.setItem('tableorder_invalid', 'invalid json');
    const result = storage.get('invalid');
    expect(result).toBeNull();
  });
});
