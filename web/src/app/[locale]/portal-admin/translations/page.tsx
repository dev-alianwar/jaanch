'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Edit, Trash2, Save, X, Globe, Search, Filter } from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import api from '@/services/api';

interface Translation {
  id: string;
  key: string;
  locale: string;
  value: string;
  category: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

const TranslationManagement: React.FC = () => {
  const [translations, setTranslations] = useState<Translation[]>([]);
  const [filteredTranslations, setFilteredTranslations] = useState<Translation[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLocale, setSelectedLocale] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const [newTranslation, setNewTranslation] = useState({
    key: '',
    locale: 'en',
    value: '',
    category: '',
    description: ''
  });

  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      router.push('/portal-admin');
      return;
    }
    
    // Set up API interceptor for admin token
    api.interceptors.request.use((config) => {
      config.headers.Authorization = `Bearer ${token}`;
      return config;
    });

    fetchTranslations();
  }, [router]);

  useEffect(() => {
    filterTranslations();
  }, [translations, searchTerm, selectedLocale, selectedCategory]);

  const fetchTranslations = async () => {
    try {
      setLoading(true);
      const response = await api.get('/translations/admin/all');
      setTranslations(response.data);
    } catch (error) {
      console.error('Failed to fetch translations:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterTranslations = () => {
    let filtered = translations;

    if (searchTerm) {
      filtered = filtered.filter(t => 
        t.key.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.value.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedLocale !== 'all') {
      filtered = filtered.filter(t => t.locale === selectedLocale);
    }

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(t => t.category === selectedCategory);
    }

    setFilteredTranslations(filtered);
  };

  const handleEdit = (translation: Translation) => {
    setEditingId(translation.id);
    setEditValue(translation.value);
    setEditDescription(translation.description || '');
  };

  const handleSave = async (id: string) => {
    try {
      await api.put(`/translations/admin/${id}`, {
        value: editValue,
        description: editDescription
      });
      
      setTranslations(translations.map(t => 
        t.id === id 
          ? { ...t, value: editValue, description: editDescription }
          : t
      ));
      
      setEditingId(null);
      setEditValue('');
      setEditDescription('');
    } catch (error) {
      console.error('Failed to update translation:', error);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this translation?')) {
      return;
    }

    try {
      await api.delete(`/translations/admin/${id}`);
      setTranslations(translations.filter(t => t.id !== id));
    } catch (error) {
      console.error('Failed to delete translation:', error);
    }
  };

  const handleAdd = async () => {
    try {
      const response = await api.post('/translations/admin', newTranslation);
      setTranslations([...translations, response.data]);
      setNewTranslation({
        key: '',
        locale: 'en',
        value: '',
        category: '',
        description: ''
      });
      setShowAddForm(false);
    } catch (error) {
      console.error('Failed to add translation:', error);
    }
  };

  const seedTranslations = async () => {
    try {
      await api.post('/translations/admin/seed');
      fetchTranslations();
      alert('Default translations seeded successfully!');
    } catch (error) {
      console.error('Failed to seed translations:', error);
    }
  };

  const categories = [...new Set(translations.map(t => t.category))].filter(Boolean);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2" style={{borderColor: '#008529'}}></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Globe className="h-6 w-6 mr-3" style={{color: '#008529'}} />
              <h1 className="text-xl font-bold text-gray-900">
                Translation Management
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="outline" onClick={seedTranslations}>
                Seed Defaults
              </Button>
              <Button onClick={() => setShowAddForm(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Translation
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Filters */}
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <Input
                  label="Search"
                  placeholder="Search translations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Language
                </label>
                <select
                  value={selectedLocale}
                  onChange={(e) => setSelectedLocale(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="all">All Languages</option>
                  <option value="en">English</option>
                  <option value="ur">Urdu</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="all">All Categories</option>
                  {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>
              
              <div className="flex items-end">
                <Button variant="outline" onClick={() => {
                  setSearchTerm('');
                  setSelectedLocale('all');
                  setSelectedCategory('all');
                }}>
                  Clear Filters
                </Button>
              </div>
            </div>
          </div>

          {/* Add Translation Form */}
          {showAddForm && (
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Translation</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Key"
                  placeholder="e.g., auth.login"
                  value={newTranslation.key}
                  onChange={(e) => setNewTranslation({...newTranslation, key: e.target.value})}
                />
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Language
                  </label>
                  <select
                    value={newTranslation.locale}
                    onChange={(e) => setNewTranslation({...newTranslation, locale: e.target.value})}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="en">English</option>
                    <option value="ur">Urdu</option>
                  </select>
                </div>
                
                <Input
                  label="Value"
                  placeholder="Translation text"
                  value={newTranslation.value}
                  onChange={(e) => setNewTranslation({...newTranslation, value: e.target.value})}
                />
                
                <Input
                  label="Category"
                  placeholder="e.g., auth, dashboard"
                  value={newTranslation.category}
                  onChange={(e) => setNewTranslation({...newTranslation, category: e.target.value})}
                />
                
                <div className="md:col-span-2">
                  <Input
                    label="Description"
                    placeholder="Optional description for translators"
                    value={newTranslation.description}
                    onChange={(e) => setNewTranslation({...newTranslation, description: e.target.value})}
                  />
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-4">
                <Button variant="outline" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
                <Button onClick={handleAdd}>
                  Add Translation
                </Button>
              </div>
            </div>
          )}

          {/* Translations Table */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Translations ({filteredTranslations.length})
                </h3>
              </div>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Key
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Language
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Value
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Category
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredTranslations.map((translation) => (
                      <tr key={translation.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {translation.key}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            translation.locale === 'en' 
                              ? 'bg-blue-100 text-blue-800' 
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {translation.locale === 'en' ? 'English' : 'Urdu'}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {editingId === translation.id ? (
                            <div className="space-y-2">
                              <textarea
                                value={editValue}
                                onChange={(e) => setEditValue(e.target.value)}
                                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                rows={2}
                              />
                              <input
                                type="text"
                                placeholder="Description (optional)"
                                value={editDescription}
                                onChange={(e) => setEditDescription(e.target.value)}
                                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                              />
                            </div>
                          ) : (
                            <div>
                              <div className="max-w-xs truncate">{translation.value}</div>
                              {translation.description && (
                                <div className="text-xs text-gray-500 mt-1">
                                  {translation.description}
                                </div>
                              )}
                            </div>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            {translation.category}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          {editingId === translation.id ? (
                            <div className="flex space-x-2">
                              <button
                                onClick={() => handleSave(translation.id)}
                                className="text-green-600 hover:text-green-900"
                              >
                                <Save className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => setEditingId(null)}
                                className="text-gray-600 hover:text-gray-900"
                              >
                                <X className="h-4 w-4" />
                              </button>
                            </div>
                          ) : (
                            <div className="flex space-x-2">
                              <button
                                onClick={() => handleEdit(translation)}
                                className="hover:opacity-80" style={{color: '#008529'}}
                              >
                                <Edit className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => handleDelete(translation.id)}
                                className="text-red-600 hover:text-red-900"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default TranslationManagement;