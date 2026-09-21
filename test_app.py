import hashlib, hmac, importlib, os, tempfile, unittest

class AppTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();os.environ.update(DB_PATH=os.path.join(self.tmp.name,'test.sqlite3'),SESSION_SECRET='s'*48,ADMIN_TOKEN='a'*48,ADMIN_USERNAME='aytanadmin',ADMIN_PASSWORD='strong-test-password',COOKIE_SECURE='0',INBOUND_WEBHOOK_SECRET='w'*48)
  import app
  self.app=importlib.reload(app);self.client=self.app.app.test_client();self.admin={'X-Admin-Token':'a'*48}
 def tearDown(self):self.tmp.cleanup()
 def chat(self,message,session_id=None,session_token=None):
  d={'message':message}
  if session_id:d.update(session_id=session_id,session_token=session_token)
  return self.client.post('/api/chat',json=d)
 def test_health_is_truthful(self):
  d=self.client.get('/api/health').get_json();self.assertFalse(d['whatsapp_connected']);self.assertFalse(d['calendar_connected']);self.assertTrue(d['automatic_lead_capture'])
 def test_capture_session_and_owner_crm(self):
  r=self.chat('Меня зовут Али. В Алматы тараканы в квартире 55 м2. Нужен выезд завтра, +7 701 123 45 67');self.assertEqual(r.status_code,200);lead=r.get_json()['lead'];self.assertEqual(lead['phone'],'+77011234567');self.assertEqual(lead['service'],'insects');self.assertEqual(lead['city'].lower(),'алматы')
  self.assertEqual(self.client.get('/api/leads').status_code,401);rows=self.client.get('/api/leads',headers=self.admin).get_json();self.assertEqual(len(rows),1);lid=rows[0]['id'];self.assertEqual(self.client.post(f'/api/leads/{lid}/status',headers=self.admin,json={'status':'В работе'}).status_code,200);self.assertEqual(self.client.get('/api/leads/export.csv',headers=self.admin).status_code,200)
 def test_private_session(self):
  d=self.chat('Нужна обработка').get_json();self.assertEqual(self.client.get('/api/session/'+d['session_id']).status_code,403);self.assertEqual(self.client.get('/api/session/'+d['session_id'],headers={'X-Session-Token':d['session_token']}).status_code,200)
 def test_signed_inbound_idempotency(self):
  body=b'{"external_id":"x-1","session_id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","source":"adapter","message":"Need rodent control"}';sig=hmac.new(b'w'*48,body,hashlib.sha256).hexdigest();h={'Content-Type':'application/json','X-Webhook-Signature':sig};self.assertFalse(self.client.post('/api/inbound',data=body,headers=h).get_json()['duplicate']);self.assertTrue(self.client.post('/api/inbound',data=body,headers=h).get_json()['duplicate'])
 def test_responsive_crm_and_knowledge(self):
  page=self.client.get('/crm');self.assertEqual(page.status_code,200);self.assertIn(b'viewport-fit=cover',page.data);self.assertIn('Сохранить'.encode(),page.data);items=self.client.get('/api/knowledge',headers=self.admin).get_json();self.assertGreaterEqual(len(items),40);created=self.client.post('/api/knowledge',headers=self.admin,json={'category':'Test','question':'Q','answer':'A'});self.assertEqual(created.status_code,201);kid=created.get_json()['id'];self.assertEqual(self.client.patch(f'/api/knowledge/{kid}',headers=self.admin,json={'active':False}).status_code,200)
 def test_admin_username_password_session_and_csrf(self):
  login=self.client.post('/api/admin/login',json={'username':'aytanadmin','password':'strong-test-password'});self.assertEqual(login.status_code,200);csrf=login.get_json()['csrf'];self.assertEqual(self.client.get('/api/admin/me').status_code,200);self.assertEqual(self.client.post('/api/knowledge',json={'category':'X','question':'Y','answer':'Z'}).status_code,403);created=self.client.post('/api/knowledge',headers={'X-CSRF-Token':csrf},json={'category':'X','question':'Y','answer':'Z'});self.assertEqual(created.status_code,201);kid=created.get_json()['id'];self.assertEqual(self.client.patch(f'/api/knowledge/{kid}',headers={'X-CSRF-Token':csrf},json={'answer':'Changed'}).status_code,200);self.assertEqual(self.client.delete(f'/api/knowledge/{kid}',headers={'X-CSRF-Token':csrf}).status_code,200)
 def test_duplicate_and_estimate(self):
  first=self.chat('Меня зовут Аян, Алматы, квартира, тараканы, завтра, +7 777 111 22 33').get_json();second=self.chat('Алматы, дом 150 м2, мыши, завтра, +7 777 111 22 33').get_json();rows=self.client.get('/api/leads',headers=self.admin).get_json();latest=next(x for x in rows if x['id']==second['lead_id']);self.assertEqual(latest['duplicate_of'],first['lead_id']);self.assertIn('40 000',latest['estimate'])
if __name__=='__main__':unittest.main()
